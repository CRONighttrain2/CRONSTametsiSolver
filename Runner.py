from operator import itemgetter

import numpy as np

import Debug
import ImageStuff
import cv2

import ProjectEnums
from DataTypes.Board import Board
from DataTypes.Point import Point
from DataTypes.Tile import Tile
from DataTypes.YellowNumber import YellowNumber
from ProjectEnums import CommonRGBColors, CommonGrayscaleColors

def add_yellow_number(board_list, y, x, outer_yellow_number_set):
    surrounding_yellow_numbers: set[YellowNumber] = set()
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            if y_offset != 0 and x_offset != 0:
                if (board_list[y + y_offset][x + x_offset] is not None) and board_list[y + y_offset][
                    x + x_offset].__class__ == YellowNumber:
                    surrounding_yellow_numbers.add(board_list[y + y_offset][x + x_offset])
    if len(surrounding_yellow_numbers) == 0:
        outer_yellow_number_set.add(YellowNumber(board_list, y, x))
    elif len(surrounding_yellow_numbers) == 1:
        surrounding_yellow_numbers.pop().add_coord(y, x)
    else:
        sorted([[yellow_number.size, yellow_number] for yellow_number in surrounding_yellow_numbers], key=itemgetter(0), reverse=True)[0][1].add_coord(y, x)
        for yellow_number in surrounding_yellow_numbers:
            for other_yellow_number in surrounding_yellow_numbers:
                if other_yellow_number != yellow_number:
                    yellow_number.add_adjacent(other_yellow_number)


def add_point(board_list, y, x, outer_point_set):
    surrounding_points: set[Point] = set()
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            if y_offset != 0 and x_offset != 0:
                if (board_list[y + y_offset][x + x_offset] is not None) and board_list[y + y_offset][
                    x + x_offset].__class__ == Point:
                    surrounding_points.add(board_list[y + y_offset][x + x_offset])
    if len(surrounding_points) == 0:
        outer_point_set.add(Point(board_list, y, x))
    elif len(surrounding_points) == 1:
        surrounding_points.pop().add_coord(y, x)
    else:
        sorted([[point.size, point] for point in surrounding_points], key=itemgetter(0), reverse=True)[0][1].add_coord(y, x)
        for point in surrounding_points:
            for other_point in surrounding_points:
                if other_point != point:
                    point.add_adjacent(other_point)

def add_tile(board_list, y: int, x: int, outer_tile_set: set[Tile]):
    surrounding_tiles: set[Tile] = set()
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            if y_offset == 0 or x_offset == 0 and not (y_offset == 0 and x_offset == 0):
                if (board_list[y + y_offset][x + x_offset] is not None) and board_list[y + y_offset][x + x_offset].__class__ == Tile:
                    surrounding_tiles.add(board_list[y + y_offset][x + x_offset])
    if len(surrounding_tiles) == 0:
        outer_tile_set.add(Tile(board_list, y, x))
    elif len(surrounding_tiles) == 1:
        surrounding_tiles.pop().add_coord(y, x)
    else:
        sorted([[tile.size, tile] for tile in surrounding_tiles], key=itemgetter(0), reverse=True)[0][1].add_coord(y, x)
        for tile in surrounding_tiles:
            for other_tile in surrounding_tiles:
                if other_tile != tile:
                    tile.add_adjacent(other_tile)

def walk_to_next_tile(y, x, y_off, x_off, board_list, current_tile: Tile):
    """uses raytracing to find if a tile is adjacent to another tile at a given point"""
    if board_list[y + y_off][x + x_off] is not None:
        return
    for off_off in range(2,6):
        if board_list[y + (y_off * off_off)][x + (x_off * off_off)].__class__ == Tile:
            current_tile.graph_node.add_node(board_list[y + (y_off * off_off)][x + (x_off * off_off)].graph_node)
        elif board_list[y + (y_off * off_off)][x + (x_off * off_off)] is not None:
            return

def find_all_colors(tile_set) -> set:
    colors = set()
    for tile in tile_set:
        tile.find_majority_color(board_data.image)
    for tile in tile_set:
        if not tile.revealed:
            colors.add(tile.color)
    return colors

if __name__ == '__main__':
    image: np.ndarray = ImageStuff.get_screenshot_on_key_press()
    board_data = Board(image)
    edge_image: np.ndarray = board_data.binary_image
    board_list = [[None for x in range(edge_image.shape[1])] for y in range(edge_image.shape[0])]

    yellow_number_set: set[YellowNumber] = set()
    for y in range(1, board_data.binary_image.shape[0] - 1):
        for x in range(1, board_data.binary_image.shape[1] - 1):
            if ImageStuff.color_equal(board_data.image[y][x], CommonRGBColors.yellow.value):
                add_yellow_number(board_list, y, x, yellow_number_set)
    for do_number_of_times in range(3):
        for yellow_number in yellow_number_set:
            yellow_number.expand(board_data.image)
    print("-cleaning yellow_numbers")
    while (sum([len(yellow_number.adjacent) for yellow_number in yellow_number_set])/len(yellow_number_set)) != 0:
        print(f'--{len(yellow_number_set)} yellow_numbers remain')
        print(f'--average number of adjacent yellow_numbers per yellow_number: {sum([len(tile.adjacent) for tile in yellow_number_set])/len(yellow_number_set)}')
        for yellow_number in yellow_number_set:
            yellow_number.overwrite_adjacent()
        #removes all tiles that no longer are on the board
        yellow_numbers_to_remove = set()
        for yellow_number in yellow_number_set:
            if board_list[yellow_number.coords[0][0]][yellow_number.coords[0][1]] != yellow_number:
                yellow_numbers_to_remove.add(yellow_number)
        for yellow_number in yellow_numbers_to_remove:
            yellow_number_set.remove(yellow_number)
        #get all new adjacent
        for yellow_number in yellow_number_set:
            for coord in yellow_number.coords:
                for y_off in range(-1, 2):
                    for x_off in range(-1, 2):
                        if (x_off == 0 or y_off == 0) and not (x_off == 0 and y_off == 0):
                            if board_list[coord[0] + y_off][coord[1] + x_off].__class__ == YellowNumber:
                                yellow_number.add_adjacent(board_list[coord[0] + y_off][coord[1] + x_off])
    print("-yellow_numbers cleaned")
    print(f'{len(yellow_number_set)} yellow numbers in board')
    for yellow_number in yellow_number_set:
        for coord in yellow_number.coords:
            board_data.binary_image[coord[0]][coord[1]] = ProjectEnums.CommonGrayscaleColors.BACKGROUND.value
    cv2.imwrite("Images/cleaned_edge_image.png", board_data.binary_image)

    #image needs to be blurred as hexagon shaped tiles will have points at every pixel along their edges if we don't
    blurry_edge_image = cv2.blur(board_data.binary_image.copy(), (5,5))
    point_image = cv2.cvtColor(board_data.binary_image.copy(), cv2.COLOR_GRAY2RGB)
    print("restore it (find points)")
    point_set = set()
    tile_set = set()
    blurry_edge_image = np.float32(blurry_edge_image)
    dst = cv2.cornerHarris(blurry_edge_image, 2,9, 0.01)
    dst = cv2.dilate(dst, None)
    point_image[dst > 0.005 * dst.max()] = CommonRGBColors.point.value
    print("and run it on the main line")
    for y in range(edge_image.shape[0]):
        for x in range(edge_image.shape[1]):
            if ImageStuff.color_equal(edge_image[y][x], CommonGrayscaleColors.TILE.value):
                point_image[y][x] = CommonRGBColors.tile.value
    cv2.imwrite("Images/point_image.png", point_image)
    new_tile = True
    for y in range(1, point_image.shape[0] - 1):
        for x in range(1, point_image.shape[1] - 1):
            if ImageStuff.color_equal(point_image[y][x], CommonRGBColors.point.value):
                add_point(board_list, y, x, point_set)
            elif ImageStuff.color_equal(point_image[y][x], CommonRGBColors.tile.value):
                add_tile(board_list, y, x, tile_set)

    print("cleaning points and tiles")
    print("-cleaning tiles")
    while (sum([len(tile.adjacent) for tile in tile_set])/len(tile_set)) != 0:
        print(f'--{len(tile_set)} tiles remain')
        print(f'--average number of adjacent tiles per tile: {sum([len(tile.adjacent) for tile in tile_set])/len(tile_set)}')
        for tile in tile_set:
            tile.overwrite_adjacent()
        #removes all tiles that no longer are on the board
        tiles_to_remove = set()
        for tile in tile_set:
            if board_list[tile.coords[0][0]][tile.coords[0][1]] != tile:
                tiles_to_remove.add(tile)
        for tile in tiles_to_remove:
            tile_set.remove(tile)
        #get all new adjacent
        for tile in tile_set:
            for coord in tile.coords:
                for y_off in range(-1, 2):
                    for x_off in range(-1, 2):
                        if (x_off == 0 or y_off == 0) and not (x_off == 0 and y_off == 0):
                            if board_list[coord[0] + y_off][coord[1] + x_off].__class__ == Tile:
                                tile.add_adjacent(board_list[coord[0] + y_off][coord[1] + x_off])
    print("-tiles cleaned")
    print("-cleaning points")
    while (sum([len(point.adjacent) for point in point_set])/len(point_set)) != 0:
        print(f'--{len(point_set)} points remain')
        print(f'--average number of adjacent points per point: {sum([len(point.adjacent) for point in point_set])/len(point_set)}')
        for point in point_set:
            point.overwrite_adjacent()
        points_to_remove = set()
        for point in point_set:
            if board_list[point.coords[0][0]][point.coords[0][1]] != point:
                points_to_remove.add(point)
        for point in points_to_remove:
            point_set.remove(point)
        for point in point_set:
            for coord in point.coords:
                for y_off in range(-1, 2):
                    for x_off in range(-1, 2):
                        if (x_off == 0 or y_off == 0) and not (x_off == 0 and y_off == 0):
                            if board_list[coord[0] + y_off][coord[1] + x_off].__class__ == Point:
                                point.add_adjacent(board_list[coord[0] + y_off][coord[1] + x_off])
    print("-points cleaned")
    print(f'{len(tile_set)} tiles and {len(point_set)} points in board')
    Debug.create_board_list_debug_image("Images/debug_image.png", point_image, board_list)

    color_set = find_all_colors(tile_set)

    print("creating graph from tile set")
    graph_node_set = set()
    if board_data.point_based_adjacency:
        print("-using point based adjacency")
        for point in point_set:
            for coord in point.coords:
                for y_off in range(-1, 2):
                    for x_off in range(-1, 2):
                        if not (x_off == 0 and y_off == 0):
                            if board_list[coord[0] + y_off][coord[1] + x_off].__class__ == Tile:
                                point.adjacent_tiles.add(board_list[coord[0] + y_off][coord[1] + x_off])
        for point in point_set:
            for tile in point.adjacent_tiles:
                graph_node_set.add(tile.graph_node)
                for other_tile in point.adjacent_tiles:
                    if other_tile != tile:
                        tile.graph_node.add_node(other_tile.graph_node)
                        other_tile.graph_node.add_node(tile.graph_node)
    else:
        print("-using non-point based adjacency")
        for tile in tile_set:
            graph_node_set.add(tile.graph_node)
            for coord in tile.coords:
                for y_off in range(-1, 2):
                    for x_off in range(-1, 2):
                        if not (x_off == 0 and y_off == 0):
                            walk_to_next_tile(coord[0], coord[1], y_off, x_off, board_list, tile)
    print("graph created")
