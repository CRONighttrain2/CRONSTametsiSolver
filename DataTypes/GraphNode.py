class Node:
    def __init__(self, tile):
        self.connected_nodes: set[Node] = set()
        self.revealed: bool = False
        self.color = None
        self.value: int = None
        self.tile = tile

    def add_connected_node(self, new_node):
        """adds a new connected node to the graph"""
        self.connected_nodes.add(new_node)

    def reveal(self):
        """sets self.revealed to true"""
        self.revealed = True

    def set_color(self, color):
        """sets color to color"""
        self.color = color