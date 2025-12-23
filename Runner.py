from operator import methodcaller

import numpy as np

import Debug
import ImageStuff
import cv2

import ProjectEnums
from DataTypes.Board import Board
from DataTypes.BoardList import BoardList
from DataTypes.Point import Point
from DataTypes.Tile import Tile
from DataTypes.YellowNumber import YellowNumber
from ProjectEnums import CommonRGBColors

def clean_up_set(board_list, set_to_clean, set_type):
    """Consolidates adjacent objects that are both set type in board list by setting coords of the smaller one to be the larger one"""
    while (sum([len(set_obj.adjacent) for set_obj in set_to_clean]) / len(set_to_clean)) != 0:
        print(f'--{len(set_to_clean)} {set_type.__name__} remain')
        print(f'--average number of adjacent {set_type.__name__}s per {set_type.__name__}: {sum([len(set_obj.adjacent) for set_obj in set_to_clean]) / len(set_to_clean)}')
        for set_obj in set_to_clean:
            set_obj.overwrite_adjacent()
        #removes all tiles that no longer are on the board
        set_obj_to_remove = set()
        for set_obj in set_to_clean:
            if board_list[set_obj.coords[0][0]][set_obj.coords[0][1]] != set_obj:
                set_obj_to_remove.add(set_obj)
        for set_obj in set_obj_to_remove:
            set_to_clean.remove(set_obj)
        #get all new adjacent
        for set_obj in set_to_clean:
            for coord in set_obj.coords:
                for y_off in range(-1, 2):
                    for x_off in range(-1, 2):
                        if (x_off == 0 or y_off == 0) and not (x_off == 0 and y_off == 0):
                            if board_list[coord[0] + y_off][coord[1] + x_off].__class__ == set_type:
                                set_obj.add_adjacent(board_list[coord[0] + y_off][coord[1] + x_off])

def walk_to_next_tile(y, x, y_off, x_off, board_list, current_tile: Tile):
    """uses raytracing to find if a tile is adjacent to another tile at a given point"""
    if board_list[y + y_off][x + x_off] is not None:
        return
    #if else is in here cause level 40's gaps between tiles were too large
    for off_off in range(2,8 if (x_off == 0 or y_off == 0) else 6):
        if board_list[y + (y_off * off_off)][x + (x_off * off_off)].__class__ == Tile:
            current_tile.graph_node.add_node(board_list[y + (y_off * off_off)][x + (x_off * off_off)].graph_node)
        elif board_list[y + (y_off * off_off)][x + (x_off * off_off)] is not None:
            return

def find_all_colors(tile_set) -> set:
    colors = set()
    for tile in tile_set:
        tile.find_majority_color(board_data.image)
    for tile in tile_set:
        if not tile.graph_node.revealed:
            colors.add(tile.color)
    return colors

if __name__ == '__main__':
    print("press left alt to take screenshot")
    image: np.ndarray = ImageStuff.get_screenshot_on_key_press()
    print("screenshot taken, starting analysis")
    board_data = Board(image)
    board_list = BoardList(board_data.image.shape)

    board_list.find_all_yellow_numbers(board_data = board_data)
    for do_number_of_times in range(3):
        for yellow_number in board_list.yellow_number_set:
            yellow_number.expand(board_data.image)
    if len(board_list.yellow_number_set) > 0:
        print("-cleaning yellow_numbers")
        clean_up_set(board_list = board_list.board_list, set_to_clean= board_list.yellow_number_set, set_type = YellowNumber)
        print("-yellow_numbers cleaned")
        print(f'{len(board_list.yellow_number_set)} yellow numbers in board')
        for yellow_number in board_list.yellow_number_set:
            for coord in yellow_number.coords:
                board_data.binary_image[coord[0]][coord[1]] = ProjectEnums.CommonGrayscaleColors.BACKGROUND.value
    cv2.imwrite("Images/cleaned_edge_image.png", board_data.binary_image)

    print("finding points")
    board_data.create_point_image()
    print("points found")
    cv2.imwrite("Images/point_image.png", board_data.points_image)

    board_list.find_all_tiles(board_data = board_data)
    board_list.find_all_points(board_data = board_data)

    print("cleaning points and tiles")
    print("-cleaning tiles")
    clean_up_set(board_list = board_list.board_list, set_to_clean= board_list.tile_set, set_type = Tile)
    print("-tiles cleaned")
    print("-cleaning points")
    clean_up_set(board_list = board_list.board_list, set_to_clean= board_list.point_set, set_type = Point)
    print("-points cleaned")
    print(f'{len(board_list.tile_set)} tiles and {len(board_list.point_set)} points in board')
    Debug.create_board_list_debug_image("Debug_images/board_list_debug_image.png", board_data.points_image, board_list.board_list)

    color_set = find_all_colors(board_list.tile_set)

    print("creating graph from tile set")
    graph_node_set = set()
    if board_data.point_based_adjacency:
        print("-using point based adjacency")
        for point in board_list.point_set:
            for coord in point.coords:
                for y_off in range(-1, 2):
                    for x_off in range(-1, 2):
                        if not (x_off == 0 and y_off == 0):
                            if board_list.board_list[coord[0] + y_off][coord[1] + x_off].__class__ == Tile:
                                point.adjacent_tiles.add(board_list.board_list[coord[0] + y_off][coord[1] + x_off])
        for point in board_list.point_set:
            for tile in point.adjacent_tiles:
                graph_node_set.add(tile.graph_node)
                for other_tile in point.adjacent_tiles:
                    if other_tile != tile:
                        tile.graph_node.add_node(other_tile.graph_node)
                        other_tile.graph_node.add_node(tile.graph_node)
    else:
        print("-using non-point based adjacency")
        for tile in board_list.tile_set:
            graph_node_set.add(tile.graph_node)
            for coord in tile.coords:
                for y_off in range(-1, 2):
                    for x_off in range(-1, 2):
                        if not (x_off == 0 and y_off == 0):
                            walk_to_next_tile(coord[0], coord[1], y_off, x_off, board_list.board_list, tile)
    print("graph created")
