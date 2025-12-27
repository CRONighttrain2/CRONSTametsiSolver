from operator import methodcaller

import numpy as np

import Debug
import ImageStuff
import cv2

import ProjectEnums
from DataTypes.Board import Board
from DataTypes.BoardList import BoardList
from DataTypes.Tile import Tile

def walk_to_next_tile(y, x, y_off, x_off, board_list, current_tile: Tile):
    """uses raytracing to find if a tile is adjacent to another tile at a given point"""
    if board_list[y + y_off][x + x_off] is not None:
        return
    #if else is in here cause level 40's gaps between tiles were too large
    for off_off in range(2,8 if (x_off == 0 or y_off == 0) else 6):
        if board_list[y + (y_off * off_off)][x + (x_off * off_off)].__class__ == Tile:
            current_tile.graph_node.add_node(new_node = board_list[y + (y_off * off_off)][x + (x_off * off_off)].graph_node)
        elif board_list[y + (y_off * off_off)][x + (x_off * off_off)] is not None:
            return

def find_all_colors(tile_set) -> set:
    colors = set()
    for tile in tile_set:
        tile.find_majority_color(image = board_data.image)
    for tile in tile_set:
        if not tile.graph_node.revealed:
            colors.add(tile.color)
    return colors

if __name__ == '__main__':
    print("press left alt to take screenshot")
    image: np.ndarray = ImageStuff.get_screenshot_on_key_press()
    print("screenshot taken, starting analysis")
    board_data = Board(board_image = image)
    board_list = BoardList(shape = board_data.image.shape)

    board_list.get_yellow_numbers(board_data = board_data)
    cv2.imwrite(filename = "Images/cleaned_edge_image.png",img = board_data.binary_image)

    print("finding points")
    board_data.create_point_image()
    print("points found")
    cv2.imwrite(filename = "Images/point_image.png",img = board_data.points_image)

    board_list.get_points(board_data = board_data)
    board_list.get_tiles(board_data = board_data)

    Debug.create_board_list_debug_image(url_name = "Debug_images/board_list_debug_image.png",image = board_data.points_image,board_list = board_list.board_list)

    color_set = find_all_colors(tile_set = board_list.tile_set)

    print("creating graph from tile set")
    graph_node_set = set()
    if board_data.point_based_adjacency:
        print("-using point based adjacency")
        for point in board_list.point_set:
            for coord in point.coords:
                for y_off in range(-1, 2):
                    for x_off in range(-1, 2):
                        if not (x_off == 0 and y_off == 0):
                            if  board_list.get_obj_at_coord({"y": coord[0] + y_off, "x": coord[1] + x_off}).__class__ == Tile:
                                point.adjacent_tiles.add( board_list.get_obj_at_coord({"y": coord[0] + y_off, "x": coord[1] + x_off}))
        for point in board_list.point_set:
            for tile in point.adjacent_tiles:
                graph_node_set.add(tile.graph_node)
                for other_tile in point.adjacent_tiles:
                    if other_tile != tile:
                        tile.graph_node.add_node(new_node = other_tile.graph_node)
                        other_tile.graph_node.add_node(new_node = tile.graph_node)
    else:
        print("-using non-point based adjacency")
        for tile in board_list.tile_set:
            graph_node_set.add(tile.graph_node)
            for coord in tile.coords:
                for y_off in range(-1, 2):
                    for x_off in range(-1, 2):
                        if not (x_off == 0 and y_off == 0):
                            walk_to_next_tile(y = coord[0], x = coord[1],y_off = y_off,x_off = x_off,board_list = board_list.board_list,current_tile = tile)
    print("graph created")
