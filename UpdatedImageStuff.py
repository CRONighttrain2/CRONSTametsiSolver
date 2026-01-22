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
                pyautogui.screenshot('Images/board_image.png')
                return cv2.imread("Images/board_image.png")
        return None

def remove_adjacency_symbol(image: ImageData, replacement_color):
    """sets the area where the symbol for adjacency would be in image to replacement color"""
    print("-removing adjacency symbol from image")
    replacement_info: dict[str,int] = {"left_y": 0, "left_x": 1800, "right_y": 80, "right_x": 1900}
    image.set_area_color(**replacement_info, fill_color = replacement_color, warped = True)

def remove_mine_counts(image: ImageData, replacement_color):
    """sets the area where the counters for the mines would be in image to replacement color"""
    print("-removing mine counts from image")
    replacement_info: dict[str, int] = {"left_y": 0, "left_x": 1800, "right_y": 400, "right_x": 1900}
    image.set_area_color(**replacement_info, fill_color = replacement_color, warped = True)

def remove_user_interface(image: ImageData, replacement_color):
    """removes all user interface elements that aren't the adjacency symbol or mine counts from image"""
    elements: dict[str, dict[str, int]] = {"return"        : {"left_y": 0,   "left_x": 0,    "right_y": 100,  "right_x": 90  },
                                           "drawtool/sound": {"left_y": 930, "left_x": 1590, "right_y": 1080, "right_x": 1920},
                                           "level name"    : {"left_y": 500, "left_x": 0,    "right_y": 1080, "right_x": 200 }}
    for element in elements:
        print(f'-removing {element} from image')
        image.set_area_color(**elements[element], fill_color= replacement_color, warped = True)