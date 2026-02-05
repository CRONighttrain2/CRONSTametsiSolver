from operator import methodcaller

from DataTypes.BoardListDataAreaClasses import BoardListDataArea, YellowArea, TileArea, VertexArea
from DataTypes.ImageData import ImageData
from DataTypes.Point import Point
from ProjectEnumsV2 import OffsetLists


class BoardGraph:
    def __init__(self, shape: ImageData):
        """
            data holder for a graph of BoardListDataArea's and helper sets for that graph to make the program "see" the board
        """
        print(f'initializing new BoardList of shape {shape}')
        self.board_graph: list[list[BoardListDataArea]] = [[None for x in range(shape.width)] for y in range(shape.height)]
        self.yellow_number_set: AreaSet = AreaSet(set_type = YellowArea, board_graph = self)
        self.tile_set: AreaSet = AreaSet(set_type = TileArea, board_graph = self)
        self.vertex_set: AreaSet = AreaSet(set_type = VertexArea, board_graph = self)

    def get_obj_at_coord(self, point : list[int] | dict[str,int] | Point):
        """
        | gets the obj at:
        | (y = list[0] | dict["y"] | Point.y, x = list[1] | dict["x"] | Point.x)
        """
        if type(point) == list:
            return self.board_graph[point[0]][point[1]]
        elif type(point) == dict:
            return self.board_graph[point["y"]][point["x"]]
        else:
            return self.board_graph[point.y][point.x]

    def set_coord(self, point : list[int] | dict[str,int] | Point, thing):
        """
        | sets the obj at:
        | (y = list[0] | dict["y"] | Point.y, x = list[1] | dict["x"] | Point.x)
        | in board_list to thing
        """
        if type(point) == list:
            self.board_graph[point[0]][point[1]] = thing
        elif type(point) == dict:
            self.board_graph[point["y"]][point["x"]] = thing
        else:
            self.board_graph[point.y][point.x] = thing

class AreaSet:
    def __init__(self, set_type: type[BoardListDataArea], board_graph: BoardGraph):
        """
        | used to store the references to and clean up the data areas on the board graph
        :param set_type: type for the set to be
        :param board_graph: reference to the board_graph the set is made by
        """
        self.area_set: set[BoardListDataArea]= set()
        self.type = set_type
        self.graph_reference = board_graph

    def add_to_set(self, current_point: Point):
        """
        | adds a new data area of type self.type to graph_reference at current_point if not next to at least one other data area
        |
        | if next to at least one other data area add to the largest one
        """
        surrounding_obj_of_type = set()
        for offset in OffsetLists.ORTHOGONAL.value:
            offset_point = current_point.offset(**offset)
            obj_at_offset = self.graph_reference.get_obj_at_coord(current_point.offset(**offset))
            if (type(obj_at_offset) == self.type) and (obj_at_offset is not self):
                surrounding_obj_of_type.add(obj_at_offset)
        if len(surrounding_obj_of_type) == 0:
            new_data_area:BoardListDataArea = self.type(board_list = self.graph_reference)
            new_data_area.add_new_point(current_point)
            self.area_set.add(new_data_area)
        else:
            max(surrounding_obj_of_type, key = methodcaller("get_size")).add_new_point(current_point)

    def find_all_type_in_image(self, image: ImageData, type_color):
        """
        sets all type_color in board_graph to self.type
        """
        for y in range(image.height):
            for x in range(image.width):
                if image.pixel_is_color(y = y, x = x, check_color = type_color):
                    current_point: Point = Point(y = y, x = x)
                    self.add_to_set(current_point = current_point)

    def add_new(self, new_element: BoardListDataArea) -> None:
        """
        adds a new object to the set
        """
        if type(new_element) == self.type:
            self.area_set.add(new_element)

    def total_adjacent(self) -> int:
        """
        returns sum of data areas in self
        """
        return sum([len(data_area.adjacent) for data_area in self.area_set])

    def average_adjacent(self) -> float:
        """
        returns average number of adjacent data areas for the data areas in self
        """
        return self.total_adjacent()/ len(self.area_set)

    def clean_set(self) -> None:
        """
        merges data areas that are next to other data areas and removes the data areas that no longer exist
        """
        print(f'-cleaning set of set type: {self.type.__name__}')
        #if we are a TileArea, get perimeter
        if self.type == TileArea:
            for tile in self.area_set:
                tile.get_perimeter()
        #areas in sets start with no adjacency data so we get that first
        self.get_adjacentcies()
        #data_area_with_no_adjacent allows us to track which data areas we no longer have to check
        data_area_with_no_adjacent: set[BoardListDataArea] = set()
        while self.total_adjacent() > 0:
            print(f'--{len(self.area_set)} {self.type.__name__}s remain in {self.type.__name__} set')
            print(f'--there is an average of {self.average_adjacent()} adjacent {self.type.__name__} per {self.type.__name__}')
            self.overwrite_smaller_adjacent()
            self.remove_non_existent_data_areas()
            self.get_adjacentcies(data_area_with_no_adjacent = data_area_with_no_adjacent)
            self.fill_data_area_with_no_adjacent(data_area_with_no_adjacent = data_area_with_no_adjacent)

    def fill_data_area_with_no_adjacent(self, data_area_with_no_adjacent: set[BoardListDataArea]) -> None:
        """
        fills the data_area_with_no_adjacent variable with the data areas that have no adjacent data areas
        """
        for data_area in self.area_set:
            if len(data_area.adjacent) == 0:
                data_area_with_no_adjacent.add(data_area)


    def overwrite_smaller_adjacent(self) -> None:
        """
        goes through each data area in area_set and tells it to overwrite its adjacent if it is the largest
        """
        for data_area in self.area_set:
            data_area.overwrite_if_adjacent_smaller()

    def get_adjacentcies(self, data_area_with_no_adjacent: set[BoardListDataArea] = None) -> None:
        """
        | fills the adjacent variable in the data areas in area_set
        :param data_area_with_no_adjacent: (optional), default: None, input for a set to keep track of the data areas with no adjacent data areas
        """
        for data_area in self.area_set:
            if (data_area_with_no_adjacent is not None) and (data_area in data_area_with_no_adjacent):
                continue
            for point in data_area.get_all_points_for_set_clean():
                for offset in OffsetLists.ORTHOGONAL.value:
                    offset_point = point.offset(**offset)
                    if self.graph_reference.get_obj_at_coord(offset_point) is not data_area:
                        data_area.add_adjacent(self.graph_reference.get_obj_at_coord(offset_point))

    def remove_non_existent_data_areas(self) -> None:
        """
        removes all data areas from outer_set which are no longer on the board_graph
        """
        data_area_to_remove: set[BoardListDataArea] = set()
        for data_area in self.area_set:
            if self.graph_reference.get_obj_at_coord(data_area.points_in_area[0]) is not data_area:
                data_area_to_remove.add(data_area)
        for data_area in data_area_to_remove:
            self.area_set.remove(data_area)