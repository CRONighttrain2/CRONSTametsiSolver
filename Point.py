class Point:
    def __init__(self, board_list, y, x):
        self.board_list = board_list
        board_list[y][x] = self
        self.coords = list()
        self.coords.append([y, x])
        self.size = 1
        self.connected_tiles = set()
        # this is made to clean up the board list
        self.adjacent = set()

    def add_coord(self, y, x):
        self.board_list[y][x] = self
        self.coords.append([y, x])
        self.size += 1

    def find_all_adjacent(self):
        new_adjacent1 = set()
        new_adjacent2 = set()
        for point in self.adjacent:
            for adjacent_point in point.adjacent:
                if adjacent_point != self:
                    new_adjacent1.add(adjacent_point)
        while len(new_adjacent1) != len(new_adjacent2):
            if len(new_adjacent2) > 0:
                new_adjacent1 = new_adjacent2.copy()
                new_adjacent2 = set()
            for point in new_adjacent1:
                for adjacent_point in point.adjacent:
                    if adjacent_point != self:
                        new_adjacent2.add(point)
        self.adjacent = new_adjacent2.copy()

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