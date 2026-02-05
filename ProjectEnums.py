import enum
from symtable import Class

import cv2


class CommonRGBColors(enum.Enum):
    """stores colors that are common in the game (in-game colors use BGR)"""
    #in game colors
    background = [35, 0, 20]
    yellow = [77, 230, 255]
    #other colors
    tile = [0, 0, 0]
    point = [0, 0, 255]
    debug_tile = [255, 0, 0]
    debug_point = [0, 255, 0]
    white = [255, 255, 255]
    debug_white = [125, 125, 125]

class CommonGrayscaleColors(enum.Enum):
    """common grayscale colors I use"""
    BACKGROUND = 255
    TILE = 0

class ImageTypes(enum.Enum):
    """made cause opencv2 doesn't specify between RGB and Gray (those are the only 2 I am using)"""
    #if we set these to the codes for the conversions between the two of them we can shorten the code
    #may cause problems later if I need more image types
    RGB = cv2.COLOR_GRAY2RGB
    GRAY = cv2.COLOR_RGB2GRAY


