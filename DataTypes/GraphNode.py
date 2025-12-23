from DataTypes.Tile import Tile


class Node:
    def __init__(self, tile):
        self.connected_nodes: set[Node] = set()
        self.node_tile: Tile = tile
        self.revealed = False

    def add_node(self, new_node):
        self.connected_nodes.add(new_node)

    def reveal(self):
        self.revealed = True