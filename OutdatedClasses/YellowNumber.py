import ColorStuff
import ProjectEnums
from DataTypes.Point import Point


class YellowNumber:
    def __init__(self, board_list, y, x):
        self.board_list = board_list
        board_list[y][x] = self
        # this is made to clean up the board list
        self.adjacent = set()
        self.size = 1
        self.coords: list[Point] = list()
        self.coords.append(Point(y = y, x = x))

    def add_coord(self, y: int, x:int):
        self.board_list[y][x] = self
        self.coords.append(Point(y = y, x = x))
        self.size += 1

    def add_adjacent(self, new):
        if new != self:
            self.adjacent.add(new)

    def overwrite_adjacent(self):
        if len(self.adjacent) == 0:
            return
        if self.size >= max([yellow_number.size for yellow_number in self.adjacent]):
            while len(self.adjacent) > 0:
                other_yellow_numbers = self.adjacent.pop()
                for other_pixel in other_yellow_numbers.coords:
                    self.board_list[other_pixel.y][other_pixel.x] = self
                    self.coords.append(other_pixel)
                    self.size += 1

    def get_size(self):
        return self.size

    def expand(self, board_image):
        """expands the yellow number into adjacent non-background, non-filled pixels on the board_list"""
        new_pixels = list()
        for pixel in self.coords:
            for y_off in range(-1, 2):
                for x_off in range(-1, 2):
                        if not (x_off == 0 and y_off == 0):
                            if self.board_list[pixel.y + y_off][pixel.x + x_off] is None:
                                if not ColorStuff.color_equal(board_image[pixel.y + y_off][pixel.x + x_off], ProjectEnums.ColorEnums.CommonGameColors.YELLOW.value):
                                    new_pixels.append(Point(y = pixel.y + y_off, x = pixel.x + x_off))
        for pixel in new_pixels:
            if pixel not in self.coords:
                self.add_coord(y = pixel.y, x = pixel.x)