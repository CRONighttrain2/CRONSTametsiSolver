from DataTypes.BoardGraph import BoardGraph
from DataTypes.BoardListDataAreaClasses import TileArea
from DataTypes.Point import Point


def walk_to_next_tile(point: Point, y_off, x_off, board_graph: BoardGraph, current_tile: TileArea):
    """uses raytracing to find if a tile is adjacent to another tile at a given point"""
    if board_graph.get_obj_at_coord(point = point.offset(y_off = y_off, x_off = x_off)) is not None:
        return
    #if else is in here cause level 40's gaps between tiles were too large
    for off_off in range(2,8 if (x_off == 0 or y_off == 0) else 6):
        current_seen_object = board_graph.get_obj_at_coord(point = point.offset(y_off = y_off * off_off, x_off = x_off * off_off))
        if current_seen_object.__class__ == TileArea:
            current_tile.graph_node.add_connected_node(new_node = current_seen_object.graph_node)
        elif current_seen_object is not None:
            return
