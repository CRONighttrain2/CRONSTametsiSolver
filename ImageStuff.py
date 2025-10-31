import cv2
import numpy as np
from pynput import keyboard
import pyautogui

from ProjectEnums import CommonRGBColors, CommonGrayscaleColors


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

def remove_UI(image: np.ndarray):
    """removes the UI from the image, image must be gray scale"""
    UI_element_bounding_box_list: dict[str, list[list[int]]] = {"return_element": [[0, 0], [90, 90]], "mine counts": [[0, 1800], [400, 1900]], "drawtool / music note" : [[930, 1590], [1070, 1910]], "level name": [[500, 0], [1070, 100]]}
    for element in UI_element_bounding_box_list.values():
        for area_y in range(element[0][0], element[1][0]):
            for area_x in range(element[0][1], element[1][1]):
                image[area_y][area_x] = CommonGrayscaleColors.background.value