import cv2
import numpy as np

import ColorStuff
import ImageStuff
import ProjectEnums


class Board:
    def __init__(self, board_image: np.ndarray):
        """Contains data on the board"""
        self.image: np.ndarray = ImageStuff.remove_UI(board_image.copy(), ProjectEnums.CommonRGBColors.background.value)
        self.point_based_adjacency: bool = self.find_adjacency_type()
        if self.find_adjacency_type():
            self.image = ImageStuff.remove_adjacency_symbol(self.image, ProjectEnums.CommonRGBColors.background.value)
        self.binary_image: np.ndarray = None
        self.create_binary_image_of_background()
        self.points_image: np.ndarray = None
    
    def find_adjacency_type(self):
        return ColorStuff.color_equal(self.image[39][1849], ProjectEnums.CommonRGBColors.yellow.value) and ColorStuff.color_equal(self.image[71][1849], ProjectEnums.CommonRGBColors.yellow.value)

    def create_binary_image_of_background(self):
        """turns image into a binary image with the background as white then stores it in binary_image"""
        image_without_mine_counts = ImageStuff.remove_mine_counts(self.image, ProjectEnums.CommonRGBColors.background.value)
        self.binary_image = ImageStuff.create_binary_image(image_without_mine_counts, ProjectEnums.CommonRGBColors.background.value)

    def create_point_image(self):
        self.points_image = cv2.cvtColor(self.binary_image.copy(), cv2.COLOR_GRAY2RGB)
        # image needs to be blurred as hexagon shaped tiles will have points at every pixel along their edges if we don't
        blurry_binary_image = cv2.blur(self.binary_image.copy(), (5, 5))
        blurry_binary_image = np.float32(blurry_binary_image)
        dst = cv2.cornerHarris(blurry_binary_image, 2, 9, 0.01)
        dst = cv2.dilate(dst, None)
        self.points_image[dst > 0.005 * dst.max()] = ProjectEnums.CommonRGBColors.point.value
        for y in range(self.binary_image.shape[0]):
            for x in range(self.binary_image.shape[1]):
                if ColorStuff.color_equal(self.binary_image[y][x], ProjectEnums.CommonGrayscaleColors.TILE.value):
                    self.points_image[y][x] = ProjectEnums.CommonRGBColors.tile.value