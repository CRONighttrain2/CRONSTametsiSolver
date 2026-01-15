from typing import overload

import cv2
import numpy as np

import ImageStuff
import ProjectEnums


class ImageData:

    def __init__(self, image: np.ndarray, image_type: ProjectEnums.ImageTypes):
        """custom class to hold images, made because opencv doesn't store certain data about images"""
        self.image: np.ndarray = image.copy()
        self.image_type: ProjectEnums.ImageTypes = image_type
        self.height: int = image.shape[0]
        self.width: int = image.shape[1]
        try:
            self.pixel_size: int = image.shape[2]
        except IndexError:
            self.pixel_size: int = 1

    @classmethod
    def convert_image_and_store(cls, image: np.ndarray, new_image_type):
        """
        coverts image to new type for storage
        :param image: input image
        :param new_image_type: cv2 image conversion int (Ie: RGB2GRAY)
        """
        converted_image = cv2.cvtColor(image.copy(), new_image_type)
        if new_image_type == cv2.COLOR_RGB2GRAY:
            image_type = ProjectEnums.ImageTypes.GRAY
        else:
            image_type = ProjectEnums.ImageTypes.RGB
        return cls(image = converted_image, image_type = image_type)


    @classmethod
    def from_imagedata(cls, image_data, new_image_type):
        """
        coverts image to new type for storage
        :param image_data: input image_data
        :param new_image_type: cv2 image conversion int (Ie: RGB2GRAY)
        """
        converted_image = cv2.cvtColor(image_data.image.copy(), new_image_type)
        if new_image_type == cv2.COLOR_RGB2GRAY:
            image_type = ProjectEnums.ImageTypes.GRAY
        else:
            image_type = ProjectEnums.ImageTypes.RGB
        return cls(image = converted_image, image_type = image_type)

    def warp_y(self, y: int) -> int:
        """returns the nearest y value on the runners screen relative to where that y would be on the authors screen"""
        return int((y/1080) * self.height)

    def warp_x(self, x: int) -> int:
        """returns the nearest x value on the runners screen relative to where that x would be on the authors screen"""
        return int((x/1920) * self.width)

    def color_valid(self, color) -> bool:
        if ImageStuff.color_rgb(color):
            if self.image_type == ProjectEnums.ImageTypes.RGB:
                if self.pixel_size == len(color):
                    return True
        else:
            if self.image_type == ProjectEnums.ImageTypes.GRAY:
                return True
        return False


    def get_pixel(self, y: int, x:int):
        """gets the color of a pixel"""
        return self.image[y][x]

    def get_pixel_warped_to_screen(self, y: int, x:int):
        """gets the color of a pixel at a position on the runners screen relative to where that position is on the authors screen"""
        return self.get_pixel(y = self.warp_y(y = y), x = self.warp_x(x = x))

    def pixel_is_color(self, y: int, x: int, color) -> bool:
        """detects if the pixel at given position is a given color"""
        return ImageStuff.color_equal(color1 = self.image[y][x], color2 = color)

    def pixel_is_color_warped_to_screen(self, y:int, x: int, color) -> bool:
        """detects if the pixel at given position is a given color on the runners screen relative to where that position is on the authors screen"""
        return self.pixel_is_color(y = self.warp_y(y = y), x = self.warp_x(x = x), color = color)

    def set_pixel(self, y: int, x: int, color):
        """| sets a pixel to a color
           :raises TypeError color is incompatible with image type"""
        #detects if color is an int or a list
        if self.color_valid(color):
            self.image[y][x] = color
        else:
            raise TypeError("color is incompatible with image type")

    def set_pixel_warped_to_screen(self, y: int, x: int, color):
        """| sets the color of a pixel at a position on the runners screen relative to where that position is on the authors screen
           :raises TypeError color is incompatible with image type
           :raises IndexError color is incorrect size for image type"""
        self.set_pixel(y = self.warp_y(y = y), x = self.warp_x(x = x), color = color)

    def set_area_color(self, left_y: int, left_x: int, right_y: int, right_x: int, color):
        """| sets an area of pixels to a color
           :raises TypeError color is incompatible with image type
           :raises ValueError left_y >= right_y or left_x >= right_x (this an error due to how the range function works)"""
        # due to how range works if right_y or right_x are too small it will return an empty list
        if left_y >= right_y or left_x >= right_x:
            raise ValueError("left_y >= right_y or left_x >= right_x")
        if self.color_valid(color):
            for y in range(left_y, right_y):
                for x in range(left_x, right_x):
                    self.set_pixel(y = y, x = x, color = color)
        else:
            raise TypeError("color is incompatible with image type")

    def set_area_color_warped_to_screen(self, left_y: int, left_x: int, right_y: int, right_x: int, color):
        """| sets an area of pixels to a color on the runners screen relative to the size and position of that area on the authors screen
           :raises TypeError color is incompatible with image type
           :raises ValueError left_y > right_y or left_x > right_x (this an error due to how the range function works)"""
        self.set_area_color(left_y = self.warp_y(y = left_y)  , left_x = self.warp_x(x = left_x),
                            right_y = self.warp_y(y = right_y), right_x = self.warp_x(x = right_x),
                            color = color)