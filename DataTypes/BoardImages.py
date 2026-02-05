import cv2
import numpy as np

from HelperClasses import ImageStuffV2
import ProjectEnumsV2
from ProjectEnumsV2 import ColorEnums
from DataTypes.ImageData import ImageData


class BoardImages:
    def __init__(self, image: np.ndarray):
        """
        holds all the images that are important for the board
        :param image: original image of the board
        """
        self.board_image: ImageData = ImageData(image = image)
        self.binary_image: ImageData = None
        self.vertex_image: ImageData = None
        self.image_width: int = self.board_image.width
        self.image_height: int = self.board_image.height
        ImageStuffV2.remove_user_interface(image = self.board_image, replacement_color = ColorEnums.CommonGameColors.BACKGROUND.value)
        if self.get_adjacency_type():
            self.point_based_adjacency: bool = True
            ImageStuffV2.remove_adjacency_symbol(image = self.board_image, replacement_color = ColorEnums.CommonGameColors.BACKGROUND.value)
        else:
            self.point_based_adjacency: bool = False
        self.create_binary_image()

    def get_adjacency_type(self) -> bool:
        """
        detects if we are using point or tile based adjacency by seeing if the icon for point based adjacency exists
        """
        return (self.board_image.pixel_is_color(y = 69, x = 1851, check_color = ColorEnums.CommonGameColors.YELLOW.value, warped = True) and
                self.board_image.pixel_is_color(y = 41, x = 1851, check_color = ColorEnums.CommonGameColors.YELLOW.value, warped = True))

    def create_binary_image(self) -> None:
        """
        creates self.binary_image from board_image with mine counts removed and the background set to white
        """
        print("creating binary image")
        self.binary_image = self.board_image.__copy__()
        ImageStuffV2.remove_mine_counts(image = self.binary_image, replacement_color = ColorEnums.CommonGameColors.BACKGROUND.value)
        self.binary_image = self.binary_image.to_binary_image(white_color = ColorEnums.CommonGameColors.BACKGROUND.value)

    def create_vertex_image(self) -> None:
        """
        creates self.point_image from the binary image by finding all the vertices in it and setting them to red
        """
        self.vertex_image = self.binary_image.__copy__()
        self.vertex_image.convert_type(ProjectEnumsV2.ImageType.RGB)
        #the binary image is too sharp to accurately find points so we need to dilate it
        dilated_image: np.ndarray = self.binary_image.image.copy()
        #IDK why it needs float 32 (something to do with corner Harris)
        #from here to line 60 have been taken from the opencv2 guide to corner harris
        dilated_image = np.float32(dilated_image)
        dilated_image = cv2.dilate(src = dilated_image, kernel = (5, 5))
        #corner harris finds the difference in the variation of intensity of an image (the numbers plugged in are from testing)
        diff_in_displace = cv2.cornerHarris(src = dilated_image, blockSize = 2, ksize = 9, k = 0.01)
        diff_in_displace = cv2.dilate(src = diff_in_displace, kernel = None)
        #finds the points where the difference in intensity is > 0.005 * diff_in_displace.max() and sets them to red
        self.vertex_image.image[diff_in_displace > 0.005 * diff_in_displace.max()] = ColorEnums.CommonProgramColors.RGBColors.VERTEX.value
        #re-adds all the tile edges cause if we don't it messes stuff up
        for y in range(self.binary_image.height):
            for x in range(self.binary_image.width):
                if (self.binary_image.pixel_is_color(y = y, x = x, check_color = ColorEnums.CommonProgramColors.GrayscaleColors.TILE.value) and
                        self.vertex_image.pixel_is_color(y = y, x = x, check_color = ColorEnums.CommonProgramColors.RGBColors.VERTEX.value)):
                    self.vertex_image.set_pixel(y = y, x = x, fill_color = ColorEnums.CommonProgramColors.RGBColors.TILE.value)
