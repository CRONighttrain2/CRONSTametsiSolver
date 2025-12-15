import cv2
import numpy as np

from DataTypes.Point import Point
from ProjectEnums import CommonRGBColors
from DataTypes.Tile import Tile


def create_board_list_debug_image(url_name: str, image, board_list):
    debug_image = image.copy()
    tile_count = 0
    yellow_number_count = 0
    point_count = 0
    tile_map: dict[Tile, int] = dict()
    point_map: dict[Point, int] = dict()
    yellow_number_map: dict[Point, int] = dict()
    for y in range(len(board_list)):
        for x in range(len(board_list[0])):
            if board_list[y][x] is None:
                debug_image[y][x] = CommonRGBColors.debug_white.value
            elif board_list[y][x].__class__ == Tile:
                if board_list[y][x] not in tile_map.keys():
                    tile_map[board_list[y][x]] = tile_count * 10
                    tile_count += 1
                    tile_count = tile_count % 24
                debug_image[y][x] = [0, 255, tile_map[board_list[y][x]]]
            elif board_list[y][x].__class__ == Point:
                if board_list[y][x] not in point_map.keys():
                    point_map[board_list[y][x]] = point_count * 10
                    point_count += 1
                    point_count = point_count % 24
                debug_image[y][x] = [255, 0, point_map[board_list[y][x]]]
            else:
                if board_list[y][x] not in yellow_number_map.keys():
                    yellow_number_map[board_list[y][x]] = yellow_number_count * 20
                    yellow_number_count += 1
                    yellow_number_count = yellow_number_count % 12
                debug_image[y][x] = [yellow_number_map[board_list[y][x]], yellow_number_map[board_list[y][x]], 255]

    cv2.imwrite(url_name, debug_image)

def see_node_connections(tile_list, image: np.ndarray):
        for tile in tile_list:
            image_copy: np.ndarray = image.copy()
            for coord in tile.coords:
                image_copy[coord[0]][coord[1]] = [0, 255, 0]
            graph_node = tile.graph_node
            for node in graph_node.connected_nodes:
                for coord in node.node_tile.coords:
                    image_copy[coord[0]][coord[1]] = CommonRGBColors.debug_tile.value
            cv2.imwrite(f'Debug_images/Adjacency_images/{tile.coords[0][0]}_{tile.coords[0][1]}_adjacency.png', image_copy)