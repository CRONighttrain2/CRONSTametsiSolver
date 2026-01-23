import enum
from symtable import Class

import cv2

class ColorEnums:
    class CommonGameColors(enum.Enum):
        """stores colors that are common in the game"""
        #for some reason these are in bgr (probably swapped when I am getting the image)
        BACKGROUND = [35, 0, 20]
        YELLOW = [77, 230, 255]
        REVEALED = [51, 51, 51]
        GRAY = [127, 127, 127]
    class CommonProgramColors:
        """stores colors that are used in this program"""
        class RGBColors(enum.Enum):
            """RGB colors"""
            TILE = [0, 0, 0]
            VERTEX = [0, 0, 255]
            WHITE = [255, 255, 255]
            DEBUG_TILE = [255, 0, 0]
            DEBUG_VERTEX = [0, 255, 0]
            DEBUG_WHITE = [125, 125, 125]
        class GrayscaleColors(enum.Enum):
            """common grayscale colors that are used in this program"""
            BACKGROUND = 255
            TILE = 0

class ImageType(enum.Enum):
    """made cause opencv2 doesn't specify between RGB and Gray (those are the only 2 I am using)"""
    #if we set these to the codes for the conversions between the two of them we can shorten the code
    #may cause problems later if I need more image types
    RGB = cv2.COLOR_GRAY2RGB
    GRAY = cv2.COLOR_RGB2GRAY
