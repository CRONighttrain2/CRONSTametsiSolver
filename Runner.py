from functools import reduce

import numpy
import numpy as np
import ImageStuff
import cv2

from Point import Point
from ProjectEnums import CommonRGBColors, CommonGrayscaleColors
from Tile import Tile


def color_equal(color1, color2):
    """finds if 2 colors are equal"""
    #checks for if we are using ints or lists
    try:
        if not len(color1) == len(color2):
            return False
    except TypeError:
        return color1 == color2
    return reduce(lambda bool1, bool2: bool1 and bool2, [color1[index] == color2[index] for index in range(0, len(color1))])

def non_background_near(edge_image, y, x) -> bool:
    """returns true if any pixels surrounding the position are not 255 (background color on the edge image)
        :param pos (y, x)
    """
    for y_off in range(-1,2):
        for x_off in range(-1,2):
            if not (x_off == 0 and y_off == 0):
                if edge_image[y + y_off][x + x_off] != CommonGrayscaleColors.background.value:
                    return True
    return False

def remove_surrounding_non_void(image, edge_image, y, x, pos_seen_set: set[str]):
    """sets position to void if it isn't already then finds all positions surrounding it and calls itself on them \n
        returns if pos is void or seen before
        :param image image of board
        :param edge_image image of board where background has been removed
        :param pos_seen_set set of positions seen
    """
    if color_equal(image[y][x], CommonRGBColors.background.value):
        return
    if f'{y},{x}' in pos_seen_set:
        return
    edge_image[y][x] = CommonGrayscaleColors.background.value
    pos_seen_set.add(f'{y},{x}')
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            if y_offset != 0 and x_offset != 0:
                remove_surrounding_non_void(image, edge_image, y + y_offset, x + x_offset, pos_seen_set)

def remove_yellow_numbers(image, edge_image):
    pos_seen = set()
    """removes yellow parts of image from edge_image"""
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if color_equal(image[y][x], CommonRGBColors.yellow.value) and not f'{y},{x}' in pos_seen:
                print(f'started removing lemon at ({x},{y})')
                remove_surrounding_non_void(image, edge_image, y, x, pos_seen)

def add_point(board_list, y, x, outer_point_set):
    point_set: set[Point] = set()
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            if y_offset != 0 and x_offset != 0:
                if (board_list[y + y_offset][x + x_offset] is not None) and board_list[y + y_offset][
                    x + x_offset].__class__ == Point:
                    point_set.add(board_list[y + y_offset][x + x_offset])
    if len(point_set) == 0:
        outer_point_set.add(Point(board_list, y, x))
    elif len(point_set) == 1:
        point_set.pop().add_coord(y, x)
    else:
        point_list = [[point.size, point] for point in point_set]
        largest_point_array = [0, None]
        for point_array in point_list:
            if point_array[0] > largest_point_array[0]:
                largest_point_array = point_array
        largest_point_array[1].add_coord(y, x)
        for point in point_set:
            for other_point in point_set:
                if other_point != point:
                    point.add_adjacent(other_point)

def add_tile(board_list, y: int, x: int, outer_tile_set: set[Tile]):
    tile_set: set[Tile] = set()
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            if y_offset != 0 and x_offset != 0:
                if (board_list[y + y_offset][x + x_offset] is not None) and board_list[y + y_offset][x + x_offset].__class__ == Tile:
                    tile_set.add(board_list[y + y_offset][x + x_offset])
    if len(tile_set) == 0:
        outer_tile_set.add(Tile(board_list, y, x))
    elif len(tile_set) == 1:
        tile_set.pop().add_coord(y, x)
    else:
        tile_list = [[tile.size, tile] for tile in tile_set]
        largest_tile_array = [0, None]
        for tile_array in tile_list:
            if tile_array[0] > largest_tile_array[0]:
                largest_tile_array = tile_array
        largest_tile_array[1].add_coord(y, x)
        for tile in tile_set:
            for other_tile in tile_set:
                if other_tile != tile:
                    tile.add_adjacent(other_tile)



if __name__ == '__main__':
    image: np.ndarray = ImageStuff.get_screenshot_on_key_press()
    edge_image: np.ndarray = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2GRAY)
    print("frying chicken in water (finding background)")
    print(image.shape)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            if color_equal(image[y][x], CommonRGBColors.background.value):
                edge_image[y][x] = CommonGrayscaleColors.background.value
            else:
                edge_image[y][x] = 0
    print("chicken fried")
    print("starting to remove lemons (removing line numbers)")
    remove_yellow_numbers(image, edge_image)
    print("lemons removed")
    ImageStuff.remove_UI(edge_image)
    #image needs to be blurred as hexagon shaped tiles will have points along every edge if we don't
    blurry_edge_image = cv2.blur(edge_image.copy(), (5,5))
    cv2.imwrite("Images/cleaned_edge_image.png", edge_image)
    point_image = cv2.cvtColor(edge_image.copy(), cv2.COLOR_GRAY2RGB)
    print("restore it (find vertices)")
    blurry_edge_image = np.float32(blurry_edge_image)
    dst = cv2.cornerHarris(blurry_edge_image, 2,9, 0.01)
    dst = cv2.dilate(dst, None)
    point_image[dst > 0.01 * dst.max()] = CommonRGBColors.point.value
    print("and run it on the main line")
    for y in range(edge_image.shape[0]):
        for x in range(edge_image.shape[1]):
            if color_equal(edge_image[y][x], CommonGrayscaleColors.tile.value):
                point_image[y][x] = CommonRGBColors.tile.value
    cv2.imwrite("Images/point_image.png", point_image)
    board_list = [[None for x in range(point_image.shape[1])] for y in range(point_image.shape[0])]
    tile_set = set()
    point_set = set()
    new_tile = True
    for y in range(1, point_image.shape[0] - 1):
        for x in range(1, point_image.shape[1] - 1):
            if color_equal(point_image[y][x], CommonRGBColors.point.value):
                add_point(board_list, y, x, point_set)
            elif color_equal(point_image[y][x], CommonRGBColors.tile.value):
                add_tile(board_list, y, x, tile_set)
    print("c")
    for tile in tile_set:
        tile.overwrite_adjacent()
    print("d")
    for point in point_set:
        point.overwrite_adjacent()
    while sum([len(tile.adjacent) for tile in tile_set])/len(tile_set) != 0:
        tile_set = set()
        point_set = set()
        for y in range(1, point_image.shape[0] - 1):
            for x in range(1, point_image.shape[1] - 1):
                surrounding = set()
                if board_list[y][x] is None:
                    continue
                for y_offset in range(-1, 2):
                    for x_offset in range(-1, 2):
                        if board_list[y + y_offset][x + x_offset] is None:
                            continue
                        if board_list[y][x].__class__ is board_list[y + y_offset][x + x_offset].__class__:
                            board_list[y][x].add_adjacent(board_list[y + y_offset][x + x_offset])
                        if board_list[y][x].__class__ is Tile:
                            tile_set.add(board_list[y][x])
                        if board_list[y][x].__class__ is Point:
                            point_set.add(board_list[y][x])
        print("c2")
        print(len(tile_set))
        print(sum([len(tile.adjacent) for tile in tile_set])/len(tile_set))
        for tile in tile_set:
            tile.overwrite_adjacent()
        print("d2")
        for point in point_set:
            point.overwrite_adjacent()


    debug_image = point_image.copy()
    tile_count = 0
    point_count = 0
    tile_map: dict[Tile, int] = dict()
    point_map: dict[Point, int] = dict()
    for y in range(len(board_list)):
        for x in range(len(board_list[0])):
            if board_list[y][x] is None:
                debug_image[y][x] = CommonRGBColors.debug_white.value
            elif board_list[y][x].__class__ == Tile:
                if board_list[y][x] not in tile_map.keys():
                    tile_map[board_list[y][x]] = tile_count * 10
                    tile_count += 1
                    tile_count = tile_count % 20
                debug_image[y][x] = [0, 255, tile_map[board_list[y][x]]]
            else:
                if board_list[y][x] not in point_map.keys():
                    point_map[board_list[y][x]] = point_count * 10
                    point_count += 1
                    point_count = point_count % 20
                debug_image[y][x] = [255, 0, point_map[board_list[y][x]]]
    cv2.imwrite("Images/debug_image4.png", debug_image)



