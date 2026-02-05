import cv2
import numpy as np
import pyautogui
from pynput import keyboard
from DataTypes.ImageData import ImageData


def get_screenshot_on_key_press() -> np.ndarray:
    """
    creates a screenshot when left alt is pressed and turns it into a numpi n dimensional array
    """
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.alt_l:
                pyautogui.screenshot('../Images/board_image.png')
                return cv2.imread("../Images/board_image.png")
        return None

def remove_adjacency_symbol(image: ImageData, replacement_color):
    """
    sets the area where the symbol for adjacency would be in image to replacement color
    """
    print("-removing adjacency symbol from image")
    replacement_info: dict[str,int] = {"y1": 0, "x1": 1800, "y2": 80, "x2": 1900}
    image.set_area_color(**replacement_info, fill_color = replacement_color, warped = True)

def remove_mine_counts(image: ImageData, replacement_color):
    """
    sets the area where the counters for the mines would be in image to replacement color
    """
    print("-removing mine counts from image")
    replacement_info: dict[str, int] = {"y1": 0, "x1": 1800, "y2": 400, "x2": 1900}
    image.set_area_color(**replacement_info, fill_color = replacement_color, warped = True)

def remove_user_interface(image: ImageData, replacement_color):
    """
    removes all user interface elements that aren't the adjacency symbol or mine counts from image
    """
    elements: dict[str, dict[str, int]] = {"return"        : {"y1": 0,   "x1": 0,    "y2": 100,  "x2": 90  },
                                           "drawtool/sound": {"y1": 930, "x1": 1590, "y2": 1080, "x2": 1920},
                                           "level name"    : {"y1": 500, "x1": 0,    "y2": 1080, "x2": 200 }}
    for element in elements:
        print(f'-removing {element} from image')
        image.set_area_color(**elements[element], fill_color= replacement_color, warped = True)

def find_all_colors(tile_set, board_images) -> set:
    """
    finds all the colors in use on the board
    """
    color_set: set = set()
    for tile in tile_set.area_set:
        tile.find_majority_color(board_image = board_images.board_image)
        color_set.add(tile.graph_node.color)
    return color_set