from operator import methodcaller

import numpy as np

from HelperClasses import ColorStuff
from DataTypes.Point import Point
from OutdatedClasses.Board import Board
from OutdatedClasses.Pixel import Pixel
from OutdatedClasses.Tile import Tile
from OutdatedClasses.YellowNumber import YellowNumber
from ProjectEnumsV2 import ColorEnums


class BoardList:
    def __init__(self, shape: tuple[int, int, int] | tuple[int, int]):
        """TODO: WRITE THIS DOCSTR"""
        #nah that docstr is never getting written >:3
        #
        # 2 months later and it still isn't written, I hate this class in particular btw :3
        self.board_list = [[None for x in range(shape[1])] for y in range(shape[0])]
        self.yellow_number_set: set[YellowNumber] = set()
        self.pixel_set: set[Pixel] = set()
        self.tile_set: set[Tile] = set()

    def get_yellow_numbers(self, board_data: Board):
        """finds all yellow_number in the yellow number image then cleans them up"""
        self.find_all_yellow_numbers(board_data = board_data)
        if len(self.yellow_number_set) > 0:
            #the yellow numbers have edges that aren't the same color so we need to blob out from them
            for yellow_number in self.yellow_number_set:
                for do_number_of_times in range(3):
                    yellow_number.expand(board_image = board_data.image)
            self.clean_yellow_number_set()
            #we need to remove the yellow numbers so it doesn't mess up the point image
            for yellow_number in self.yellow_number_set:
                for pixel in yellow_number.coords:
                    board_data.binary_image[pixel.y][pixel.x] = ColorEnums.CommonGameColors.BACKGROUND.value


    def get_pixels(self, board_data: Board):
        """finds all points in the point image then cleans them up"""
        self.find_all_pixels(board_data = board_data)
        self.clean_pixel_set()

    def get_tiles(self, board_data: Board):
        """finds all tiles in the point image then cleans them up"""
        self.find_all_tiles(board_data = board_data)
        for tile in self.tile_set:
            tile.get_perimeter()
        self.clean_tile_set()

    def clean_set(self, outer_set:set, set_type):
        """Consolidates adjacent objects that are both set type in board list by setting coords of the smaller one to be the larger one"""
        print(f'-cleaning set of type {set_type.__name__}')
        set_obj_w_no_adjacent: set = set()
        while (sum([len(set_obj.adjacent) for set_obj in outer_set]) / len(outer_set)) != 0:
            print(f'--{len(outer_set)} {set_type.__name__} remain')
            print(f'--average number of adjacent {set_type.__name__}s per {set_type.__name__}: {sum([len(set_obj.adjacent) for set_obj in outer_set]) / len(outer_set)}')
            for set_obj in outer_set:
                set_obj.overwrite_adjacent()
            #removes all set_obj that no longer are on the board
            set_obj_to_remove: set = set()
            for set_obj in outer_set:
                if self.get_obj_at_coord(set_obj.coords[0].as_dict()) != set_obj:
                        set_obj_to_remove.add(set_obj)
            for set_obj in set_obj_to_remove:
                outer_set.remove(set_obj)
            #get all new adjacent
            for set_obj in outer_set:
                if set_obj not in set_obj_w_no_adjacent:
                    for pixel in set_obj.coords:
                        for y_off in range(-1, 2):
                            for x_off in range(-1, 2):
                                if (x_off == 0 or y_off == 0) and not (x_off == 0 and y_off == 0):
                                    if self.get_obj_at_coord(pixel.offset(y_off, x_off).as_dict()).__class__ == set_type:
                                        set_obj.add_adjacent(self.get_obj_at_coord(pixel.offset(y_off, x_off).as_dict()))
            #if the set_obj has no more adjacent, remove it from our searches
            for set_obj in outer_set:
                if len(set_obj.adjacent) == 0:
                    set_obj_w_no_adjacent.add(set_obj)
            #made to stop an infinite loop caused by my terrible code
            #adjacent_to_add: set = set()
            #for set_obj in outer_set:
            #    for adjacent_obj in set_obj.adjacent:
            #        if adjacent_obj not in outer_set:
            #            adjacent_to_add.add(adjacent_obj)
            #for adjacent in adjacent_to_add:
            #    outer_set.add(adjacent)
        print(f'-set of type {set_type.__name__} cleaned')
        print(f'{len(outer_set)} in set of type {set_type.__name__}')

    def clean_yellow_number_set(self):
        self.clean_set(outer_set = self.yellow_number_set, set_type = YellowNumber)

    def clean_tile_set(self):
        print(f'-cleaning set of type Tile')
        tiles_with_no_adjacent: set[Tile] = set()
        while (sum([len(tile.adjacent) for tile in self.tile_set]) / len(self.tile_set)) != 0:
            print(f'--{len(self.tile_set)} tiles remain')
            print(f'--average number of adjacent tiles per tile: {(sum([len(tile.adjacent) for tile in self.tile_set]) / len(self.tile_set))}')
            for tile in self.tile_set:
                tile.overwrite_adjacent()
            #removes all tile that no longer are on the board
            tiles_to_remove_from_set: set[Tile] = set()
            for tile in self.tile_set:
                if self.get_obj_at_coord(tile.coords[0].as_dict()) is not tile:
                    tiles_to_remove_from_set.add(tile)
            for tile in tiles_to_remove_from_set:
                self.tile_set.remove(tile)
            for tile in self.tile_set:
                if tile not in tiles_with_no_adjacent:
                    for pixel in tile.perimeter:
                        for y_off in range(-1, 2):
                            for x_off in range(-1, 2):
                                if (x_off == 0 or y_off == 0) and not (x_off == 0 and y_off == 0):
                                    if self.get_obj_at_coord(pixel.offset(y_off, x_off).as_dict()).__class__ == Tile:
                                        tile.add_adjacent(self.get_obj_at_coord(pixel.offset(y_off, x_off).as_dict()))
            #if the set_obj has no more adjacent, remove it from our searches
            for set_obj in self.tile_set:
                if len(set_obj.adjacent) == 0:
                    tiles_with_no_adjacent.add(set_obj)
        print(f'-set of type Tile cleaned')
        print(f'{len(self.tile_set)} in set of type Tile')


    def clean_pixel_set(self):
        self.clean_set(outer_set = self.pixel_set, set_type = Pixel)

    def find_all_in_image(self ,image: np.ndarray , obj_color: list[int] | tuple[int], outer_set: set, set_type):
        """finds all obj_color in image and maps it onto board_list with type set_type"""
        for y in range(len(self.board_list)):
            for x in range(len(self.board_list[0])):
                if ColorStuff.color_equal(image[y][x], obj_color):
                    self.add_to_set(y = y, x = x, outer_set = outer_set, set_type = set_type)

    def find_all_yellow_numbers(self, board_data: Board):
        """
        | goes through board_data.image and finds all yellow numbers in it
        |
        | (this is just a find_all_in_image call but with preset values)"""
        self.find_all_in_image(image = board_data.image, obj_color = ColorEnums.CommonGameColors.YELLOW.value, outer_set = self.yellow_number_set, set_type = YellowNumber)

    def find_all_tiles(self, board_data: Board):
        """
        | goes through board_data.points_image and finds all tiles in it
        |
        | (this is just a find_all_in_image call but with preset values)"""
        self.find_all_in_image(image = board_data.points_image, obj_color = ColorEnums.CommonProgramColors.RGBColors.TILE.value, outer_set = self.tile_set, set_type = Tile)

    def find_all_pixels(self, board_data: Board):
        """
        | goes through board_data.points_image and finds all points in it
        |
        | (this is just a find_all_in_image call but with preset values)"""
        self.find_all_in_image(image = board_data.points_image, obj_color = ColorEnums.CommonProgramColors.RGBColors.VERTEX.value, outer_set = self.pixel_set, set_type = Pixel)

    def add_to_set(self, y, x, outer_set, set_type):
        """| Adds a new object of set_type to the outer_set if it is not next to another object of set_type
           |
           | if it is next to another object of set type it adds that coord to that object"""
        surronding_objects = set()
        for y_off in range(-1, 2):
            for x_off in range(-1, 2):
                if (x_off == 0 or y_off == 0) and not (x_off == 0 and y_off == 0):
                    if (self.get_obj_at_coord({"x": x + x_off, "y": y + y_off}) is not None) and self.get_obj_at_coord({"x": x + x_off, "y": y + y_off}).__class__ == set_type:
                        surronding_objects.add(self.get_obj_at_coord({"x": x + x_off, "y": y + y_off}))
        if len(surronding_objects) == 0:
            outer_set.add(set_type(board_list = self.board_list, y = y,x = x))
        elif len(surronding_objects) == 1:
            surronding_objects.pop().add_coord(y = y,x = x)
        else:
            max(surronding_objects, key=methodcaller("get_size")).add_coord(y = y, x = x)
            for pixel in surronding_objects:
                for other_pixel in surronding_objects:
                    if other_pixel != pixel:
                        pixel.add_adjacent(new = other_pixel)

    def get_obj_at_coord(self, point : list[int] | dict[str,int] | Point):
        """
        | gets the obj at:
        | (y = list[0] | dict["y"] | Point.y, x = list[1] | dict["x"] | Point.x)
        """
        if type(point) == list:
            return self.board_list[point[0]][point[1]]
        elif type(point) == dict:
            return self.board_list[point["y"]][point["x"]]
        else:
            return self.board_list[point.y][point.x]

    def set_coord(self, point : list[int] | dict[str,int] | Point, thing):
        """
        | sets the point:
        | (y = list[0] | dict["y"] | Point.y, x = list[1] | dict["x"] | Point.x)
        | in board_list to thing
        """
        if type(point) == list:
            self.board_list[point[0]][point[1]] = thing
        elif type(point) == dict:
            self.board_list[point["y"]][point["x"]] = thing
        else:
            self.board_list[point.y][point.x] = thing