class Point:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def __eq__(self, other):
        return (self.y == other.y) and (self.x == other.x)

    def __hash__(self):
        return hash(f'{self.y},{self.x}')

    def __repr__(self):
        return f'(y:{self.y},x:{self.x})'

    def as_dict(self) -> dict[str, int]:
        return {"y": self.y, "x": self.x}

    def copy(self):
        return Point(y = self.y, x = self.x)

    def offset(self, y_off: int, x_off: int):
        return Point(y = self.y + y_off, x = self.x + x_off)