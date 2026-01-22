from functools import reduce

import numpy as np


def color_rgb(color):
    """detects if a color is not an int"""
    try:
        len(color)
    except TypeError:
        return False
    return True


def color_equal(color1, color2):
    """checks if 2 colors are equal"""
    #checks if the colors are the same length
    try:
        if not len(color1) == len(color2):
            return False
    except TypeError:
        return color1 == color2
    return reduce(lambda bool1, bool2: bool1 and bool2, [color1[index] == color2[index] for index in range(0, len(color1))])


def color_size_correct(image: np.ndarray, color) -> bool:
    """checks if the color is the correct size for the image"""
    #make sure that the color is the correct size for the colorspace of the image
    if len(image.shape) == 2 and type(color) != int:
        return False
    elif len(image.shape) > 2:
        if type(color) == int:
            return False
        elif image.shape[2] != len(color):
            return False
    return True
