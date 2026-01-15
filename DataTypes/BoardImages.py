import numpy as np

import ProjectEnums
from DataTypes.ImageData import ImageData


class BoardImages:
    def __init__(self, image: np.ndarray):
        self.board_image: ImageData = ImageData(image, ProjectEnums.ImageTypes.RGB)
        self.point_based_adjacency: bool = self.get_adjacency_type()
        # if self.point_based_adjacency is too fast and the var isn't set when this is called
        # if self.get_adjacency_type():



    def get_adjacency_type(self):
        """detects if we are using point or tile based adjacency by seeing if the icon for point based adjacency exists"""
        return (self.board_image.pixel_is_color_warped_to_screen(y = 69, x = 1851, color = ProjectEnums.CommonRGBColors.yellow.value) and
                self.board_image.pixel_is_color_warped_to_screen(y = 41, x = 1851, color = ProjectEnums.CommonRGBColors.yellow.value))