import GraphNode

class Tile:
    def __init__(self, board_list, y, x):
        self.board_list = board_list
        board_list[y][x] = self
        # this is made to clean up the board list
        self.adjacent = set()
        self.size = 1
        self.coords = list()
        self.coords.append([y, x])
        self.graph_node: GraphNode.Node = GraphNode.Node(self)
        self.color = None
        self.revealed = False

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
        if self.size >= max([tile.size for tile in self.adjacent]):
            while len(self.adjacent) > 0:
                other_tile = self.adjacent.pop()
                for coord in other_tile.coords:
                    self.board_list[coord[0]][coord[1]] = self
                    self.coords.append([coord[0], coord[1]])
                    self.size += 1

    def find_majority_color(self, image):
        color_map: dict[str, int] = dict()
        for coord in self.coords:
            if str(image[coord[0]][coord[1]]) not in color_map.keys():
                color_map.update({str(image[coord[0]][coord[1]]): 0})
            color_map[str(image[coord[0]][coord[1]])] += 1
            if color_map[str(image[coord[0]][coord[1]])] > len(self.coords)/2:
                break
        biggest_color = ["", 0]
        for color in color_map.keys():
            if color_map[color] > biggest_color[1]:
                biggest_color[0] = color
                biggest_color[1] = color_map[color]
        color_list = [int(num) for num in biggest_color[0].replace("[","").replace("]","").split()]
        if color_list == [51, 51, 51]:
            self.color = "51, 51, 51"
            self.revealed = True
        elif color_list[0] == color_list[1] == color_list[2]:
            self.color = "120, 120, 120"
        else:
            self.color = f'{color_list[0]}, {color_list[1]}, {color_list[2]}'