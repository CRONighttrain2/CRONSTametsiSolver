import enum

class CommonRGBColors(enum.Enum):
    """stores colors that are common in the game"""
    background = [35, 0, 20]
    black = [0, 0, 0]
    yellow = [77, 230, 255]
    point_red = [0, 0, 255]

class CommonGrayscaleColors(enum.Enum):
    background = 255
    tile = 0