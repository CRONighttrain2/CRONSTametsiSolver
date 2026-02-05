class Point:
    def __init__(self, y: int, x: int):
        """data holder for x y pairs"""
        self.y = y
        self.x = x

    def __eq__(self, other):
        return (self.y == other.y) and (self.x == other.x)

    def __hash__(self):
        return hash(f'{self.y},{self.x}')

    def __repr__(self):
        return f'(y:{self.y},x:{self.x})'

    def as_dict(self, y_name: str = "y", x_name:str = "x") -> dict[str, int]:
        """
        | returns self as a dict: {"y", "x"}
        :param y_name: (optional), default: "y", if changed renames "y" in dict to input
        :param x_name: (optional), default: "x", if changed renames "x" in dict to input
        """
        return {y_name: self.y, x_name: self.x}

    def copy(self):
        """
        returns a copy of self
        """
        return Point(y = self.y, x = self.x)

    def offset(self, y_off: int, x_off: int):
        """
        returns an offset copy of self
        """
        return Point(y = self.y + y_off, x = self.x + x_off)