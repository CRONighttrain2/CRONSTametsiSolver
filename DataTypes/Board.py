import numpy as np

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
        return ImageStuff.color_equal(self.image[39][1849], ProjectEnums.CommonRGBColors.yellow.value) and ImageStuff.color_equal(self.image[71][1849], ProjectEnums.CommonRGBColors.yellow.value)

    def create_binary_image_of_background(self):
        """turns image into a binary image with the background as white then stores it in binary_image"""
        image_without_mine_counts = ImageStuff.remove_mine_counts(self.image, ProjectEnums.CommonRGBColors.background.value)
        self.binary_image = ImageStuff.create_binary_image(image_without_mine_counts, ProjectEnums.CommonRGBColors.background.value)

