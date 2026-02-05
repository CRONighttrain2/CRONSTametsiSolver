import numpy as np

import Debug
import cv2

from HelperClasses import ImageStuffV2
from OutdatedClasses.Board import Board
from OutdatedClasses.BoardList import BoardList
from OutdatedClasses.Tile import Tile

if __name__ == '__main__':
    print("press left alt to take screenshot")
    image: np.ndarray = ImageStuffV2.get_screenshot_on_key_press()
    print("screenshot taken, starting analysis")
    board_data = Board(board_image = image)
    board_list = BoardList(shape = board_data.image.shape)

    board_list.get_yellow_numbers(board_data = board_data)
    cv2.imwrite(filename ="../Images/cleaned_edge_image.png", img = board_data.binary_image)

    print("finding points")
    board_data.create_point_image()
    print("points found")
    cv2.imwrite(filename ="../Images/point_image.png", img = board_data.points_image)

    board_list.get_pixels(board_data = board_data)
    board_list.get_tiles(board_data = board_data)

    Debug.create_board_list_debug_image(url_name = "Debug_images/board_list_debug_image.png",image = board_data.points_image,board_list = board_list.board_list)

    #color_set = find_all_colors(tile_set = board_list.tile_set)

    print("creating graph from tile set")
    graph_node_set = set()
    if board_data.point_based_adjacency:
        print("-using point based adjacency")
        for point in board_list.pixel_set:
            for pixel in point.coords:
                for y_off in range(-1, 2):
                    for x_off in range(-1, 2):
                        if not (x_off == 0 and y_off == 0):
                            if  board_list.get_obj_at_coord(pixel.offset(y_off, x_off).as_dict()).__class__ == Tile:
                                point.adjacent_tiles.add( board_list.get_obj_at_coord(pixel.offset(y_off, x_off).as_dict()))
        for point in board_list.pixel_set:
            for tile in point.adjacent_tiles:
                graph_node_set.add(tile.graph_node)
                for other_tile in point.adjacent_tiles:
                    if other_tile != tile:
                        tile.graph_node.add_connected_node(new_node = other_tile.graph_node)
                        other_tile.graph_node.add_connected_node(new_node = tile.graph_node)
    else:
        print("-using non-point based adjacency")
        for tile in board_list.tile_set:
            graph_node_set.add(tile.graph_node)
            #for pixel in tile.coords:
                #for y_off in range(-1, 2):
                    #for x_off in range(-1, 2):
                        #if not (x_off == 0 and y_off == 0):
                            #walk_to_next_tile(y = pixel.y, x = pixel.x, y_off = y_off, x_off = x_off, board_list = board_list.board_list, current_tile = tile)
    print("graph created")
