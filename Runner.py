from functools import reduce

import numpy as np
import ImageStuff
import cv2

from ProjectEnums import CommonColors


def color_equal(color1, color2):
    """finds if 2 colors are equal"""
    if not len(color1) == len(color2):
        return False
    return reduce(lambda bool1, bool2: bool1 and bool2, [color1[index] == color2[index] for index in range(0, len(color1))])

def non_background_near(image, y, x) -> bool:
    """returns true if any pixels surrounding the position are true
        :param pos (y, x)
    """
    for y_off in range(-1,2):
        for x_off in range(-1,2):
            if not (x_off == 0 and y_off == 0):
                if image[y + y_off][x + x_off] != 255:
                    return True
    return False

def remove_UI(image):
    """removes the UI from the image"""
    UI_element_area_list = [[[0, 0], [90, 90]],[[0, 1800], [400, 1900]],[[930, 1590], [1070, 1910]],[[500, 0], [1070, 100]]]
    for element in UI_element_area_list:
        for area_y in range(element[0][0], element[1][0]):
            for area_x in range(element[0][1], element[1][1]):
                image[area_y][area_x] = 255

def remove_surrounding_non_void(image, edge_image, y, x, pos_seen_set: set[str]):
    """sets position to void if it isn't already then finds all positions surrounding it and calls itself on them \n
        returns if pos is void or seen before
        :param image image of board
        :param edge_image image of board where background has been removed
        :param pos_seen_set set of positions seen
    """
    if color_equal(image[y][x], CommonColors.background.value):
        return
    if f'{y},{x}' in pos_seen_set:
        return
    edge_image[y][x] = 255
    pos_seen_set.add(f'{y},{x}')
    for y_offset in range(-1, 2):
        for x_offset in range(-1, 2):
            if y_offset != 0 and x_offset != 0:
                remove_surrounding_non_void(image, edge_image, y + y_offset, x + x_offset, pos_seen_set)

def remove_yellow_numbers(image, edge_image):
    pos_seen = set()
    """removes yellow parts of image from edge_image"""
    for y in range(0, len(edge_image)):
        for x in range(0, len(edge_image[0])):
            if color_equal(image[y][x], CommonColors.yellow.value) and not f'{y},{x}' in pos_seen:
                print(f'started removing lemon at ({x},{y})')
                remove_surrounding_non_void(image, edge_image, y, x, pos_seen)



if __name__ == '__main__':
    image = ImageStuff.get_screenshot_on_key_press()
    edge_image = cv2.cvtColor(image.copy(), cv2.COLOR_RGB2GRAY)
    print("frying chicken in water (finding background)")
    for y in range(0, len(edge_image)):
        for x in range(0, len(edge_image[0])):
            if color_equal(image[y][x], CommonColors.background.value):
                edge_image[y][x] = 255
            else:
                edge_image[y][x] = 0
    print("chicken fried")
    print("starting to remove lemons (removing line numbers)")
    remove_yellow_numbers(image, edge_image)
    print("lemons removed")
    remove_UI(edge_image)
    blurry_edge_image = cv2.blur(edge_image.copy(), (5,5))
    cv2.imwrite("cleaned_edge_image.png", edge_image)
    print("restore it (find vertices)")
    point_image = cv2.cvtColor(edge_image.copy(), cv2.COLOR_GRAY2RGB)
    blurry_edge_image = np.float32(blurry_edge_image)
    dst = cv2.cornerHarris(blurry_edge_image, 2,9, 0.01)
    dst = cv2.dilate(dst, None)
    point_image[dst > 0.01 * dst.max()] = CommonColors.point_red.value
    cv2.imwrite("point_image.png", point_image)
    print("and run it on the main line")


