import GraphNode
from DataTypes.Tile import Tile


class Point:
    def __init__(self, board_list, y, x):
        self.board_list = board_list
        board_list[y][x] = self
        self.coords = list()
        self.coords.append([y, x])
        self.size = 1
        self.connected_tiles = set()
        # this is made to clean up the board list
        self.adjacent: set[Point] = set()
        # used when making graph of nodes
        self.adjacent_tiles: set[Tile] = set()

    def add_coord(self, y, x):
        self.board_list[y][x] = self
        self.coords.append([y, x])
        self.size += 1

    def get_size(self):
        return self.size

    def add_adjacent(self, new):
        if new != self:
            self.adjacent.add(new)

    def overwrite_adjacent(self):
        if len(self.adjacent) == 0:
            return
        if self.size >= max([point.size for point in self.adjacent]):
            while len(self.adjacent) > 0:
                other_point = self.adjacent.pop()
                for coord in other_point.coords:
                    self.board_list[coord[0]][coord[1]] = self
                    self.coords.append([coord[0], coord[1]])
                    self.size += 1