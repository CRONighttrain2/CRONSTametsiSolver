import enum
from symtable import Class


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
    RGB = 0
    GRAY = 1

