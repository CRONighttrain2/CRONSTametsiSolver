from functools import singledispatch, singledispatchmethod, wraps
from operator import methodcaller

import ImageStuff
from DataTypes.Board import Board
from DataTypes.Point import Point
from DataTypes.Tile import Tile
from DataTypes.YellowNumber import YellowNumber
from ProjectEnums import CommonRGBColors


class BoardList:
    def __init__(self, shape: tuple[int, int, int] | tuple[int, int]):
        """TODO: WRITE THIS DOCSTR"""
        #nah that docstr is never getting written >:3
        self.board_list = [[None for x in range(shape[1])] for y in range(shape[0])]
        self.yellow_number_set: set[YellowNumber] = set()
        self.point_set: set[Point] = set()
        self.tile_set: set[Tile] = set()

    def find_all_in_image(self,image, obj_color, outer_set, set_type):
        """finds all obj_color in image and maps it onto board_list with type set_type"""
        for y in range(len(self.board_list)):
            for x in range(len(self.board_list[0])):
                if ImageStuff.color_equal(image[y][x], obj_color):
                    self.add_to_set(y = y, x = x, outer_set = outer_set, set_type = set_type)

    def find_all_yellow_numbers(self, board_data: Board):
        """
        | goes through board_data.image and finds all yellow numbers in it
        |
        | (this is just a find_all_in_image call but with preset values)"""
        self.find_all_in_image(image = board_data.image, obj_color = CommonRGBColors.yellow.value, outer_set = self.yellow_number_set, set_type = YellowNumber)

    def find_all_tiles(self, board_data: Board):
        """
        | goes through board_data.points_image and finds all tiles in it
        |
        | (this is just a find_all_in_image call but with preset values)"""
        self.find_all_in_image(image = board_data.points_image, obj_color = CommonRGBColors.tile.value, outer_set = self.tile_set, set_type = Tile)

    def find_all_points(self, board_data: Board):
        """
        | goes through board_data.points_image and finds all points in it
        |
        | (this is just a find_all_in_image call but with preset values)"""
        self.find_all_in_image(image = board_data.points_image, obj_color = CommonRGBColors.point.value, outer_set = self.point_set, set_type = Point)

    def add_to_set(self, y, x, outer_set, set_type):
        """| Adds a new object of set_type to the outer_set if it is not next to another object of set_type
           |
           | if it is next to another object of set type it adds that coord to that object"""
        surrounding_pixels = set()
        for y_off in range(-1, 2):
            for x_off in range(-1, 2):
                if (x_off == 0 or y_off == 0) and not (x_off == 0 and y_off == 0):
                    if (self.get_coord({"x": x + x_off, "y": y + y_off}) is not None) and self.get_coord({"x": x + x_off, "y": y + y_off}).__class__ == set_type:
                        surrounding_pixels.add(self.get_coord({"x": x + x_off, "y": y + y_off}))
        if len(surrounding_pixels) == 0:
            outer_set.add(set_type(self.board_list, y, x))
        elif len(surrounding_pixels) == 1:
            surrounding_pixels.pop().add_coord(y, x)
        else:
            max(surrounding_pixels, key=methodcaller("get_size")).add_coord(y, x)
            for pixel in surrounding_pixels:
                for other_pixel in surrounding_pixels:
                    if other_pixel != pixel:
                        pixel.add_adjacent(other_pixel)

    @singledispatchmethod
    def get_coord(self, coord:list[int]):
        """
        | implementation 1:
        | inputs = (coord: list[int], thing: Any)
        | gets the point at y = coord[0],x = coord[1] in board list
        |
        | implementation 2:
        | inputs = (y: int, x: int)
        | gets the point at y = y,x = x in board list
        |
        | implementation 3:
        | inputs = (coord: dict[y: int, x: int])
        | gets the point at y = coord["y"],x = coord["x"] in board list"""
        return self.board_list[coord[0]][coord[1]]

    @get_coord.register
    def _(self, coord: dict):
        return self.board_list[coord["y"]][coord["x"]]

    @get_coord.register
    def _(self, y:int, x: int):
        return self.board_list[y][x]


    @singledispatchmethod
    def set_coord(self, coord: list[int], thing):
        """
        | implementation 1:
        | inputs = (coord: list[int], thing: Any)
        | sets the point at y = coord[0],x = coord[1] in board list to thing
        |
        | implementation 2:
        | inputs = (y: int, x: int , thing: Any)
        | sets the point at y = y,x = x in board list to thing
        |
        | implementation 3:
        | inputs = (coord: dict[y: int, x: int] , thing: Any)
        | sets the point at y = coord["y"],x = coord["x"] in board list to thing"""
        self.board_list[coord[0]][coord[1]] = thing

    @set_coord.register
    def _(self, y: int, x: int, thing):
        self.board_list[y][x] = thing

    @set_coord.register
    def _(self, coord: dict, thing):
        self.board_list[coord["y"]][coord["x"]] = thing