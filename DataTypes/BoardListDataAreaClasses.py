from typing import override
from DataTypes.BoardList import BoardList
from DataTypes.GraphNode import Node
from DataTypes.ImageData import ImageData
from DataTypes.Point import Point
from ProjectEnums import ColorEnums


class BoardListDataArea:
    def __init__(self, board_list: BoardList):
        self.points_in_area: list[Point] = []
        self.adjacent: set[BoardListDataArea] = set()
        self.size: int = 0
        self.board_list: BoardList = board_list

    def add_new_point(self, new_point: dict[str, int] | Point) -> None:
        """sets board list y, x to this obj and adds the coord to points_in_area"""
        if type(new_point) == Point:
            self.points_in_area.append(new_point.copy())
        else:
            self.points_in_area.append(Point(y = new_point["y"], x = new_point["x"]))
        self.size += 1
        self.board_list.set_coord(point = new_point,thing = self)

    def add_adjacent(self, new_adjacent) -> None:
        """adds a new obj to adjacent"""
        if new_adjacent is not self:
            self.adjacent.add(new_adjacent)

    def overwrite_all_adjacent(self) -> None:
        """overwrites all adjacent with self"""
        while len(self.adjacent) > 0:
            adjacent_obj: BoardListDataArea = self.adjacent.pop()
            for point in adjacent_obj.points_in_area:
                self.add_new_point(new_point = point)

    def overwrite_if_adjacent_smaller(self):
        """overwrites all adjacent with self if self.size is larger than the largest adjacent.size"""
        if len(self.adjacent) > 0:
            if self.size >= max([adjacent.size for adjacent in self.adjacent]):
                self.overwrite_all_adjacent()

class TileArea(BoardListDataArea):
    def __init__(self, board_list: BoardList):
        super().__init__(board_list = board_list)
        self.graph_node = Node()
        self.perimeter: list[Point] = list()

    def find_majority_color(self, board_image: ImageData) -> None:
        """
        finds the color that has the largest presence in the tile

        :param board_image: original image of the board
        """
        color_map: dict[str, int] = dict()
        for point in self.points_in_area:
            #Point.as_dict() will return a dict w/ {"y", "x"} so we can unwrap it into get_pixel
            pixel_color = str(board_image.get_pixel(**point.as_dict()))
            if pixel_color not in color_map.keys():
                color_map[pixel_color] = 0
            color_map[pixel_color] += 1
            if sum(color_map.values()) > len(self.points_in_area)/4:
                break
        biggest_color = max({color_map[key]: key for key in color_map.keys()}.items())[1]
        color_list = [int(num) for num in biggest_color.replace("[","").replace("]","").split()]
        if color_list == ColorEnums.CommonGameColors.REVEALED.value:
            self.graph_node.set_color(color = ColorEnums.CommonGameColors.REVEALED.value)
            self.graph_node.reveal()
        # the gray in this game will always have r == g == b but offset by a random value
        elif color_list[0] == color_list[1] == color_list[2]:
            self.graph_node.set_color(color = ColorEnums.CommonGameColors.GRAY.value)
        else:
            self.graph_node.set_color(color = color_list)

    def get_perimeter(self):
        """fills self.perimeter with all points on the perimeter"""
        for point in self.points_in_area:
            for y_off in range(-1, 2):
                for x_off in range(-1, 2):
                    if (x_off == 0 or y_off == 0) and not (x_off == 0 and y_off == 0):
                        offset_point: Point = point.offset(y_off = y_off, x_off = x_off)
                        if self.board_list.get_obj_at_coord(point = offset_point) is not self:
                            self.perimeter.append(point)
                            return

    @override
    def overwrite_all_adjacent(self):
        while len(self.adjacent) > 0:
            other_tile = self.adjacent.pop()
            for point in other_tile.perimeter:
                self.perimeter.append(point)
            for point in other_tile.points_in_area:
                self.add_new_point(point)

class VertexArea(BoardListDataArea):
    def __init__(self, board_list: BoardList):
        super().__init__(board_list = board_list)

class YellowArea(BoardListDataArea):
    def __init__(self, board_list:BoardList):
        super().__init__(board_list = board_list)

    def expand(self, board_image: ImageData):
        """
        expands this area to adjacent non-background pixels

        :param board_image: original image of the board
        """
        new_points: list[Point] = []
        for point in self.points_in_area:
            for y_off in range(-1, 2):
                for x_off in range(-1, 2):
                        if not (x_off == 0 and y_off == 0):
                            new_point = point.offset(y_off = y_off, x_off = x_off)
                            #Point.as_dict() will return a dict w/ {"y", "x"} so we can unwrap it into pixel_is_color
                            if not board_image.pixel_is_color(**new_point.as_dict(), check_color = ColorEnums.CommonGameColors.BACKGROUND.value):
                                new_points.append(new_point)
        for new_point in new_points:
            self.add_new_point(new_point = new_point)

    def remove_from_image(self, binary_image: ImageData):
        """
        removes the yellow numbers from the image

        :param binary_image: binary_image from BoardImages obj
        """
        for point in self.points_in_area:
            #Point.as_dict() will return a dict w/ {"y", "x"} so we can unwrap it into set_pixel
            binary_image.set_pixel(**point.as_dict(),fill_color = ColorEnums.CommonProgramColors.GrayscaleColors.BACKGROUND.value)
