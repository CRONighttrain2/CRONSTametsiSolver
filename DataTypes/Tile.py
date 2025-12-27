import numpy as np

from DataTypes.GraphNode import Node


class Tile:
    def __init__(self, board_list, y, x):
        self.board_list = board_list
        board_list[y][x] = self
        # this is made to clean up the board list
        self.adjacent = set()
        self.size = 1
        self.coords = list()
        self.coords.append([y, x])
        self.color = None
        self.graph_node = Node()

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
        if self.size >= max([tile.size for tile in self.adjacent]):
            while len(self.adjacent) > 0:
                other_tile = self.adjacent.pop()
                for coord in other_tile.coords:
                    self.board_list[coord[0]][coord[1]] = self
                    self.coords.append([coord[0], coord[1]])
                    self.size += 1

    def find_majority_color(self, image: np.ndarray):
        color_map: dict[str, int] = dict()
        for coord in self.coords:
            if str(image[coord[0]][coord[1]]) not in color_map.keys():
                color_map.update({str(image[coord[0]][coord[1]]): 0})
            color_map[str(image[coord[0]][coord[1]])] += 1
            #if we have looked at a quarter of the tile we already will know the most prevalent color
            if sum(color_map.values()) > (image.shape[0] * image.shape[1])/4:
                break
        biggest_color = max({color_map[key]: key for key in color_map.keys()}.items())[1]
        color_list = [int(num) for num in biggest_color.replace("[","").replace("]","").split()]
        #pre-revealed tiles are always colored [51,51,51]
        if color_list == [51, 51, 51]:
            self.color = "51, 51, 51"
            self.graph_node.reveal()
        #every other tile where the colors are all the same will always be gray but the actual values in the gray vary on a per-tile basis so we need to do this
        elif color_list[0] == color_list[1] == color_list[2]:
            self.color = "120, 120, 120"
        #all other colors
        else:
            self.color = f'{color_list[0]}, {color_list[1]}, {color_list[2]}'