class Node:
    def __init__(self):
        self.connected_nodes: set[Node] = set()
        self.revealed = False
        self.color = None
        self.value = None

    def add_connected_node(self, new_node):
        self.connected_nodes.add(new_node)

    def reveal(self):
        self.revealed = True

    def set_color(self, color):
        self.color = color