import cv2
from pynput import keyboard
import pyautogui

def get_screenshot_on_key_press():
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.alt_l:
                pyautogui.screenshot('board_image.png')
                return cv2.imread("board_image.png")
        return None
