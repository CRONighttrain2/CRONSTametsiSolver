from DataTypes.Point import Point


class BoardList:
    def __init__(self):
        print("BALTIMORE - Big bill hells cars")

    def get_obj_at_coord(self, point : list[int] | dict[str,int] | Point):
        """
        | gets the obj at:
        | (y = list[0] | dict["y"] | Point.y, x = list[1] | dict["x"] | Point.x)
        """
        if type(point) == list:
            return self.board_list[point[0]][point[1]]
        elif type(point) == dict:
            return self.board_list[point["y"]][point["x"]]
        else:
            return self.board_list[point.y][point.x]

    def set_coord(self, point : list[int] | dict[str,int] | Point, thing):
        """
        | sets the point:
        | (y = list[0] | dict["y"] | Point.y, x = list[1] | dict["x"] | Point.x)
        | in board_list to thing
        """
        if type(point) == list:
            self.board_list[point[0]][point[1]] = thing
        elif type(point) == dict:
            self.board_list[point["y"]][point["x"]] = thing
        else:
            self.board_list[point.y][point.x] = thing