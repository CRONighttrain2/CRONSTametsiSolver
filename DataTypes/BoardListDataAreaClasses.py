from typing import override

from DataTypes.GraphNode import Node
from DataTypes.ImageData import ImageData
from DataTypes.Point import Point
from ProjectEnumsV2 import ColorEnums, OffsetLists

class BoardListDataArea:
    def __init__(self, board_list):
        self.points_in_area: list[Point] = []
        self.adjacent: set[BoardListDataArea] = set()
        self.size: int = 0
        self.board_list = board_list

    def get_size(self):
        """
        returns self.size used in creating the board graph
        """
        return self.size

    def add_new_point(self, new_point: dict[str, int] | Point) -> None:
        """
        sets board list y, x to this obj and adds the coord to points_in_area
        """
        if type(new_point) == Point:
            self.points_in_area.append(new_point.copy())
        else:
            self.points_in_area.append(Point(y=new_point["y"], x=new_point["x"]))
        self.size += 1
        self.board_list.set_coord(point=new_point, thing=self)

    def add_adjacent(self, new_adjacent) -> None:
        """
        adds a new obj to adjacent
        """
        if (self is not new_adjacent) and (type(self) == type(new_adjacent)):
            self.adjacent.add(new_adjacent)

    def overwrite_all_adjacent(self) -> None:
        """
        overwrites all adjacent with self
        """
        while len(self.adjacent) > 0:
            adjacent_obj: VertexArea = self.adjacent.pop()
            for point in adjacent_obj.points_in_area:
                self.add_new_point(new_point=point)

    def overwrite_if_adjacent_smaller(self):
        """
        overwrites all adjacent with self if self.size is larger than the largest adjacent.size
        """
        #needs to be less than or equal so we can resolve the issue of two areas being the same size
        if len(self.adjacent) > 0:
            if self.size >= max([adjacent.get_size() for adjacent in self.adjacent]):
                self.overwrite_all_adjacent()

    # the following functions have been made so tile can override them
    def get_all_points_for_set_clean(self) -> list[Point]: return self.points_in_area
    def find_majority_color(self, board_image: ImageData) -> None: return None
    def get_perimeter(self) -> None: return None

    # the following functions have been made so YellowArea can override them
    def expand(self, board_image: ImageData): return None
    def remove_from_image(self, binary_image: ImageData) -> None: return None

class TileArea(BoardListDataArea):
    def __init__(self, board_list):
        super().__init__(board_list = board_list)
        self.adjacent: set[TileArea] = set()
        # - perimeter allows us to not have to go over every point in the tile
        self.perimeter: list[Point] =  list()
        # - graph node is the node used in the creation of the graph of tiles
        self.graph_node: Node = Node(self)

    @override
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
        #converts the color from a str to a list so I don't have to deal with np.ndarrays
        color_as_list = [int(num) for num in biggest_color.replace("[","").replace("]","").split()]
        if color_as_list == ColorEnums.CommonGameColors.REVEALED.value:
            self.graph_node.set_color(color = ColorEnums.CommonGameColors.REVEALED.value)
            self.graph_node.reveal()
        # the gray in this game will always have r == g == b but offset by a random value
        elif color_as_list[0] == color_as_list[1] == color_as_list[2]:
            self.graph_node.set_color(color = ColorEnums.CommonGameColors.GRAY.value)
        else:
            self.graph_node.set_color(color = color_as_list)

    @override
    def get_perimeter(self):
        """
        fills self.perimeter with all points on the perimeter
        """
        for point in self.points_in_area:
            for offset in OffsetLists.SURROUNDING.value:
                #offset uses the notation {"y_off","x_off"} so we can unwrap it into the offset function of point as that is the vars it takes
                offset_point: Point = point.offset(**offset)
                if self.board_list.get_obj_at_coord(point = offset_point) is not self:
                    self.perimeter.append(point)
                    break

    @override
    def overwrite_all_adjacent(self):
        """
        override of overwrite_all_adjacent made to account for tile's perimeter var
        """
        while len(self.adjacent) > 0:
            other_tile = self.adjacent.pop()
            for point in other_tile.perimeter:
                self.perimeter.append(point)
            for point in other_tile.points_in_area:
                self.add_new_point(point)

    @override
    def get_all_points_for_set_clean(self) -> list[Point]:
        """
        override of get_all_points_for_set_clean made so tiles use a perimeter system rather than going through every point in it
        """
        return self.perimeter


class YellowArea(BoardListDataArea):
    def __init__(self, board_list):
        super().__init__(board_list = board_list)
        self.adjacent: set[YellowArea] = set()

    @override
    def expand(self, board_image: ImageData) -> None:
        """
        expands this area to adjacent non-background pixels

        :param board_image: original image of the board
        """
        new_points: list[Point] = []
        for point in self.points_in_area:
            for offset in OffsetLists.SURROUNDING.value:
                #offset uses the notation {"y_off","x_off"} so we can unwrap it into the offset function of point as that is the vars it takes
                new_point = point.offset(**offset)
                #Point.as_dict() will return a dict w/ {"y", "x"} so we can unwrap it into pixel_is_color
                if not board_image.pixel_is_color(**new_point.as_dict(), check_color = ColorEnums.CommonGameColors.BACKGROUND.value):
                    new_points.append(new_point)
        for new_point in new_points:
            self.add_new_point(new_point = new_point)

    def remove_from_image(self, binary_image: ImageData) -> None:
        """
        removes the yellow numbers from the image

        :param binary_image: binary_image from BoardImages obj
        """
        for point in self.points_in_area:
            #Point.as_dict() will return a dict w/ {"y", "x"} so we can unwrap it into set_pixel
            binary_image.set_pixel(**point.as_dict(),fill_color = ColorEnums.CommonProgramColors.GrayscaleColors.BACKGROUND.value)

class VertexArea(BoardListDataArea):
    def __init__(self, board_list):
        super().__init__(board_list = board_list)
        self.adjacent: set[VertexArea] = set()