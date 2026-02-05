import cv2
import numpy as np

import Debug
from HelperClasses import ImageStuffV2
from DataTypes.BoardGraph import BoardGraph
from DataTypes.BoardImages import BoardImages
from ProjectEnumsV2 import ColorEnums

if __name__ == '__main__':
    print("press left alt to take screenshot")
    image: np.ndarray = ImageStuffV2.get_screenshot_on_key_press()
    print("creating board images")
    board_images: BoardImages = BoardImages(image = image)
    board_graph: BoardGraph = BoardGraph(shape = board_images.board_image)
    print("board images created")

    cv2.imwrite(filename = "cleaned_board_image.png", img = board_images.board_image.image)
    cv2.imwrite("edge_image.png", board_images.binary_image.image)

    print("finding all yellow numbers")
    board_graph.yellow_number_set.find_all_type_in_image(image = board_images.board_image, type_color = ColorEnums.CommonGameColors.YELLOW.value)
    if len(board_graph.yellow_number_set.area_set) > 0:
        board_graph.yellow_number_set.clean_set()
        for yellow_area in board_graph.yellow_number_set.area_set:
            for iterator in range(2):
                yellow_area.expand(board_images.board_image)
            yellow_area.remove_from_image(board_images.binary_image)
    print("yellow numbers removed")
    cv2.imwrite(filename = "Images/cleaned_edge_image.png", img = board_images.binary_image.image)
#
    print("creating vertex image")
    board_images.create_vertex_image()
    print("vertex image created")
    cv2.imwrite(filename = "Images/point_image.png", img = board_images.vertex_image.image)
#
    print("finding all tiles")
    board_graph.tile_set.find_all_type_in_image(board_images.vertex_image, ColorEnums.CommonProgramColors.RGBColors.TILE.value)
    board_graph.tile_set.clean_set()
    print("found all tiles")

    print("finding all vertexes")
    board_graph.vertex_set.find_all_type_in_image(board_images.vertex_image, ColorEnums.CommonProgramColors.RGBColors.VERTEX.value)
    board_graph.vertex_set.clean_set()
    print("found all vertexes")

    Debug.create_board_list_debug_image(url_name = "Debug_images/board_list_debug_image.png",image = board_images.vertex_image.image,board_list = board_graph.board_graph)