from typing import Any

import cv2
import numpy as np

import ColorStuff
import ProjectEnums
from ProjectEnums import ImageType


class ImageData:

    def __init__(self, image: np.ndarray):
        """custom class to hold images, made because opencv doesn't store certain data about images"""
        self.image: np.ndarray = image.copy()
        self.image_type: ImageType = ImageType.RGB if ColorStuff.color_rgb(color = image[0][0]) else ImageType.GRAY
        self.height: int = image.shape[0]
        self.width: int = image.shape[1]
        if ColorStuff.color_rgb(color = image[0][0]):
            self.pixel_size: int = image.shape[2]
        else:
            self.pixel_size: int = 1

    @classmethod
    def convert_image_and_store(cls, image: np.ndarray, image_type: ImageType):
        """
        | coverts image to new type for storage
        | if image is already that type, it doesn't convert the image
        :param image: input image
        :param image_type: cv2 image conversion int (Ie: RGB2GRAY)
        """
        if ((ColorStuff.color_rgb(image[0][0]) and image_type == ImageType.GRAY) or
            (not ColorStuff.color_rgb(image[0][0]) and image_type == ImageType.RGB)):
            converted_image = cv2.cvtColor(image.copy(), image_type.value)
            return cls(image = converted_image)
        else:
            return cls(image = image.copy())

    def to_binary_image(self, white_color):
        """creates a new image data then turns its image into a binary image of the original where pixels that are color
        are white and pixels that aren't are black then returns the new image"""
        new_image = self.__copy__()
        new_image.convert_type(new_image_type = ImageType.GRAY)
        for y in range(self.height):
            for x in range(self.width):
                if self.pixel_is_color(y = y, x = x, check_color = white_color):
                    new_image.set_pixel(y = y, x = x, fill_color = ProjectEnums.ColorEnums.CommonProgramColors.GrayscaleColors.BACKGROUND.value)
                else:
                    new_image.set_pixel(y = y, x = x, fill_color = ProjectEnums.ColorEnums.CommonProgramColors.GrayscaleColors.TILE.value)
        return new_image

    def convert_type(self, new_image_type: ImageType) -> None:
        """converts current image into a new type"""
        if self.image_type is not new_image_type:
            self.image = cv2.cvtColor(self.image, new_image_type.value)
            self.image_type = new_image_type
            if ColorStuff.color_rgb(color = self.image[0][0]):
                self.pixel_size: int = self.image.shape[2]
            else:
                self.pixel_size: int = 1

    def color_valid(self, color) -> bool:
        """
        checks if the color is a valid color for the image_type of this imageData
        """
        if ColorStuff.color_rgb(color):
            if self.image_is_type(image_type = ImageType.RGB):
                if self.pixel_size == len(color):
                    return True
        else:
            if self.image_is_type(image_type = ImageType.GRAY):
                return True
        return False

    def image_is_type(self, image_type: ImageType) -> bool:
        """
        detects if self.image_type is image_type
        """
        return self.image_type == image_type

    def warp_y(self, y: int) -> int:
        """
        returns the nearest y value on the runners screen relative to where that y would be on the authors screen
        """
        return int(y * (self.height / 1080))

    def warp_x(self, x: int) -> int:
        """
        returns the nearest x value on the runners screen relative to where that x would be on the authors screen
        """
        return int(x * (self.width / 1920))

    def get_pixel(self, y: int, x:int, warped: bool = None):
        """
        gets the color of a pixel

        :param y: y value of coord to set
        :param x: x value of coord to set
        :param warped: (optional), if true, scales the y and x relative to the runners screen size
        """
        if warped:
            y = self.warp_y(y = y)
            x = self.warp_x(x = x)
        return self.image[y][x]

    def pixel_is_color(self, y: int, x: int, check_color, warped: bool = None) -> bool:
        """
        detects if the pixel at given position is check_color

        :param y: y value of coord to set
        :param x: x value of coord to set
        :param check_color: color to check
        :param warped: (optional), if true, scales the y and x relative to the runners screen size
        """
        if warped:
            y = self.warp_y(y = y)
            x = self.warp_x(x = x)
        return ColorStuff.color_equal(color1 = self.image[y][x], color2 = check_color)

    def set_pixel(self, y: int, x: int, fill_color, warped: bool = False) -> None:
        """
        Sets a pixel to a color

        :param y: y value of coord to set
        :param x: x value of coord to set
        :param fill_color: color to fill pixel with
        :param warped: (optional), if true: scales the y and x relative to the runners screen size
        :raises TypeError if color is incompatible with image type
        """
        if not  self.color_valid(fill_color):
            raise TypeError("color is incompatible with image type")
        if warped:
            y = self.warp_y(y = y)
            x = self.warp_x(x = x)
        self.image[y][x] = fill_color

    def set_area_color(self, y1: int, x1: int, y2: int, x2: int, fill_color: Any, warped: bool = None) -> None:
        """
        sets an area of pixels to a color

        :param y1: y1 value of area to fill
        :param x1: x1 value of area to fill
        :param y2: y2 value of area to fill
        :param x2: x2 value of area to fill
        :param fill_color: color to fill with
        :param warped: (optional), if true: scales the area relative to the runners screen size
        :raises ValueError if y1 == y2 or x1 == x2 (this an error due to how the range function works)
        :raises TypeError if color is incompatible with image type
        """
        # due to how range works if the y values or x values are equal range will return an empty list and there is nothing we can do about it
        if y1 == y2 or x1 == x2:
            raise ValueError(f'y1 == y2 or x1 == x2 in set area color for input ({x1},{y1}), ({x2},{y2})')
        if not self.color_valid(color = fill_color):
            raise TypeError(f'fill color {fill_color} is invalid for image of type {"gray" if ColorStuff.color_rgb(fill_color) else "rgb"}')
        # due to how range works if y1 > y2 range will return an empty list
        if y1 > y2:
            holder = y2
            y2 = y1
            y1 = holder
        # due to how range works if x1 > x2 range will return an empty list
        if x1 > x2:
            holder = x2
            x2 = x1
            x1 = holder
        if warped:
            y1, x1  = self.warp_y(y = y1), self.warp_x(x = x1)
            y2, x2 = self.warp_y(y = y2), self.warp_x(x = x2)
        for y in range(y1, y2):
            for x in range(x1, x2):
                self.set_pixel(y = y, x = x, fill_color = fill_color)

    def set_pixel_color_if_color(self, x: int, y: int, fill_color, check_color, warped: bool = False) -> None:
        """
        sets pixel at (x,y) to fill_color if its color is check_color
        :param x: x value of pixel
        :param y: y value of pixel
        :param fill_color: color to fill with
        :param check_color: color to fill
        :param warped: (optional), if true: scales the y and x relative to the runners screen size
        :raises TypeError if either color is incompatible with image type
        """
        if not self.color_valid(color = fill_color):
            raise TypeError(f'fill color {fill_color} is invalid for image of type {"gray" if ColorStuff.color_rgb(fill_color) else "rgb"}')
        if not self.color_valid(color = check_color):
            raise TypeError(f'check color {check_color} is invalid for image of type {"gray" if ColorStuff.color_rgb(check_color) else "rgb"}')
        if warped:
            y = self.warp_y(y = y)
            x = self.warp_x(x = x)
        if ColorStuff.color_equal(color1 = self.get_pixel(y = y, x = x), color2 = check_color):
            self.set_pixel(y = y, x = x, fill_color = fill_color)

    def set_pixels_in_area_if_color(self, y1: int, x1: int, y2: int, x2: int, fill_color, check_color, warped: bool = None) -> None:
        """
        sets any pixels that are check_color in area to fill_color

        :param y1: y1 value of area to fill
        :param x1: x1 value of area to fill
        :param y2: y2 value of area to fill
        :param x2: x2 value of area to fill
        :param fill_color: color to fill with
        :param check_color: color to fill
        :param warped: (optional), if true: scales the area relative to the runners screen size
        :raises ValueError if left_y >= right_y or left_x >= right_x (this an error due to how the range function works)
        :raises TypeError if either color is incompatible with image type
        """
        # due to how range works if the y values or x values are equal range will return an empty list and there is nothing we can do about it
        if y1 == y2 or x1 == x2:
            raise ValueError(f'y1 == y2 or x1 == x2 in set area color for input ({x1},{y1}), ({x2},{y2})')
        if not self.color_valid(color = fill_color):
            raise TypeError(f'fill color {fill_color} is invalid for image of type {"gray" if ColorStuff.color_rgb(fill_color) else "rgb"}')
        if not self.color_valid(color = check_color):
            raise TypeError(f'check color {check_color} is invalid for image of type {"gray" if ColorStuff.color_rgb(check_color) else "rgb"}')
        # due to how range works if y1 > y2 range will return an empty list
        if y1 > y2:
            holder = y2
            y2 = y1
            y1 = holder
        # due to how range works if x1 > x2 range will return an empty list
        if x1 > x2:
            holder = x2
            x2 = x1
            x1 = holder
        if warped:
            y1, x1  = self.warp_y(y = y1), self.warp_x(x = x1)
            y2, x2 = self.warp_y(y = y2), self.warp_x(x = x2)
        for y in range(y1, y2):
            for x in range(x1, x2):
                self.set_pixel_color_if_color(y = y, x = x, fill_color = fill_color, check_color = check_color)


    def __copy__(self):
        """creates a copy of the current ImageData"""
        return ImageData(image = self.image.copy())