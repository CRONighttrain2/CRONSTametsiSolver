import cv2
import numpy as np

import ProjectEnums
from HelperClasses.ColorStuff import color_equal, color_size_correct

def remove_UI(image: np.ndarray, replacement_color)-> np.ndarray:
    """creates a copy of image and removes the UI from the copy"""
    #make sure that the color is the correct size for the colorspace of the image
    if not color_size_correct(image, replacement_color):
        raise TypeError("color is not the same size as colors in image")

    new_image = image.copy()

    UI_element_bounding_box_list: dict[str, dict[str, dict[str,int]]] = {"return_element": {"left_edge" : {"y": 0, "x": 0},
                                                                                            "right_edge" : {"y": 100, "x": 90}},
                                                                    "drawtool / music note" : {"left_edge" : {"y": 930, "x": 1590},
                                                                                               "right_edge" : {"y": 1080, "x": 1920}},
                                                                    "level name": {"left_edge" : {"y": 500, "x": 0},
                                                                                   "right_edge" : {"y": 1080, "x": 200}}}
    for element in UI_element_bounding_box_list.values():
        #the y's and x's are divided by numbers because my original screen I used for this was 1920 x 1080
        for area_y in range(int(image.shape[0] * (element["left_edge"]["y"] / 1080)), int(image.shape[0] * (element["right_edge"]["y"] / 1080))):
            for area_x in range(int(image.shape[1] * (element["left_edge"]["x"] / 1920)), int(image.shape[1] * (element["right_edge"]["x"] / 1920))):
                new_image[area_y][area_x] = replacement_color
    return new_image

def remove_mine_counts(image: np.ndarray, replacement_color)-> np.ndarray:
    """| creates a copy of image and removes the mine count from the copy
       | made so I can preserve them on the original image but remove the mine count on the binary image"""
    #make sure that the color is the correct size for the colorspace of the image
    if not color_size_correct(image, replacement_color):
        raise TypeError("color is not the same size as colors in image")

    new_image = image.copy()
    #the y's and x's are divided by numbers because my original screen I used for this was 1920 x 1080
    element_bounding_box: dict[str,dict[str,int]] = {"left_edge" : {"y": 0, "x": 1800},"right_edge" :  {"y": 400, "x": 1900}}
    for area_y in range(int(image.shape[0] * (element_bounding_box["left_edge"]["y"]/1080)), int(image.shape[0] * (element_bounding_box["right_edge"]["y"]/1080))):
        for area_x in range(int(image.shape[1] * (element_bounding_box["left_edge"]["x"]/1920)), int(image.shape[1] * (element_bounding_box["right_edge"]["x"]/1920))):
            new_image[area_y][area_x] = replacement_color
    return new_image

def remove_adjacency_symbol(image: np.ndarray, replacement_color)-> np.ndarray:
    """| creates a copy of image and removes the UI from the copy
       | made cause it was messing up the finding of the yellow numbers"""
    #make sure that the color is the correct size for the colorspace of the image
    if not color_size_correct(image, replacement_color):
        raise TypeError("color is not the same size as colors in image")

    new_image = image.copy()
    #the y's and x's are divided by numbers because my original screen I used for this was 1920 x 1080
    element_bounding_box: dict[str,dict[str,int]] = {"left_edge" : {"y": 0, "x": 1800},"right_edge" :  {"y": 80, "x": 1900}}
    for area_y in range(int(image.shape[0] * (element_bounding_box["left_edge"]["y"]/1080)), int(image.shape[0] * (element_bounding_box["right_edge"]["y"]/1080))):
        for area_x in range(int(image.shape[1] * (element_bounding_box["left_edge"]["x"]/1920)), int(image.shape[1] * (element_bounding_box["right_edge"]["x"]/1920))):
            new_image[area_y][area_x] = replacement_color
    return new_image


def create_binary_image(image: np.ndarray, color):
    """creates a copy of image that is grayscale and turns all pixels that are color in that image into white and all others into black
        :raise TypeError if color is not the same size as colors in image
        """
    #make sure that the color is the correct size for the colorspace of the image
    if not color_size_correct(image, color):
        raise TypeError("color is not the same size as colors in image")
    #create new image
    new_image: np.ndarray = None
    if len(image.shape) == 2:
        new_image = image.copy()
    else:
       new_image = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2GRAY)
    #fill new image
    for y, row in enumerate(image):
        for x, pixel in enumerate(row):
            if color_equal(pixel, color):
                new_image[y][x] = ProjectEnums.CommonGrayscaleColors.BACKGROUND.value
            else:
                new_image[y][x] = ProjectEnums.CommonGrayscaleColors.TILE.value
    return new_image
