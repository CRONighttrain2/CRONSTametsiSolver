import ImageStuff
import ProjectEnums


class YellowNumber:
    def __init__(self, board_list, y, x):
        self.board_list = board_list
        board_list[y][x] = self
        # this is made to clean up the board list
        self.adjacent = set()
        self.size = 1
        self.coords = list()
        self.coords.append([y, x])

    def add_coord(self, y, x):
        self.board_list[y][x] = self
        self.coords.append([y, x])
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
                for coord in other_yellow_numbers.coords:
                    self.board_list[coord[0]][coord[1]] = self
                    self.coords.append([coord[0], coord[1]])
                    self.size += 1

    def get_size(self):
        return self.size

    def expand(self, board_image):
        """expands the yellow number into adjacent non-background, non-filled pixels on the board_list"""
        new_coords = list()
        for coord in self.coords:
            for y_off in range(-1, 2):
                for x_off in range(-1, 2):
                        if not (x_off == 0 and y_off == 0):
                            if self.board_list[coord[0] + y_off][coord[1] + x_off] is None:
                                if not ImageStuff.color_equal(board_image[coord[0] + y_off][coord[1] + x_off], ProjectEnums.CommonRGBColors.background.value):
                                    new_coords.append([coord[0] + y_off, coord[1] + x_off])
        for coord in new_coords:
            if coord not in self.coords:
                self.add_coord(coord[0],coord[1])