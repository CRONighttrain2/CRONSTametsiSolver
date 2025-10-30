from Point import Point


class Tile:
    def __init__(self, outline: list[Point]):
        self.outline: list[Point] = outline
        self.innerPositions = set()