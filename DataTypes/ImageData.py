from typing import overload

import cv2
import numpy as np

import ProjectEnums


class ImageData:
    def __init__(self, image: np.ndarray, image_type: ProjectEnums.ImageTypes):
        """holds an image"""
        self.image = image.copy()
        self.image_type = image_type

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
        return cls(image=converted_image, image_type=image_type)


    @classmethod
    def covert_other_ImageData(cls, image_data, new_image_type):
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
        return cls(image=converted_image, image_type=image_type)


    def width(self):
        return self.image.shape[1]

    def height(self):
        return self.image.shape[0]