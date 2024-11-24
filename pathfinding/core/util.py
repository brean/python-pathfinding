import copy
import math
from typing import List, Tuple

from .node import Node


# square root of 2 for diagonal distance
SQRT2 = math.sqrt(2)

Coords = Tuple[float, float]


def backtrace(node: Node) -> List[Node]:
    """
    Backtrace according to the parent records and return the path.
    (including both start and end nodes)
    """
    path = [node]
    while node.parent:
        node = node.parent
        path.append(node)
    path.reverse()
    return path


def bi_backtrace(node_a: Node, node_b: Node) -> List[Node]:
    """
    Backtrace from start and end node, returns the path for bi-directional A*
    (including both start and end nodes)
    """
    path_a = backtrace(node_a)
    path_b = backtrace(node_b)
    path_b.reverse()
    return path_a + path_b


def raytrace(coords_a: Coords, coords_b: Coords) -> List[Coords]:
    line = []
    x0, y0 = coords_a
    x1, y1 = coords_b

    dx = x1 - x0
    dy = y1 - y0

    t = 0
    grid_pos = [x0, y0]
    t_for_one = \
        abs(1.0 / dx) if dx > 0 else 10000, \
        abs(1.0 / dy) if dy > 0 else 10000

    frac_start = (x0 + .5) - x0, (y0 + .5) - y0
    t_for_next_border = [
        (1 - frac_start[0] if dx < 0 else frac_start[0]) * t_for_one[0],
        (1 - frac_start[1] if dx < 0 else frac_start[1]) * t_for_one[1]
    ]

    step = \
        1 if dx >= 0 else -1, \
        1 if dy >= 0 else -1

    while t <= 1:
        line.append(copy.copy(grid_pos))
        index = 0 if t_for_next_border[0] <= t_for_next_border[1] else 1
        t = t_for_next_border[index]
        t_for_next_border[index] += t_for_one[index]
        grid_pos[index] += step[index]
    return line


def bresenham(coords_a: Coords, coords_b: Coords) -> List[Coords]:
    '''
    Given the start and end coordinates, return all the coordinates lying
    on the line formed by these coordinates, based on Bresenham's algorithm.
    http://en.wikipedia.org/wiki/Bresenham's_line_algorithm#Simplification
    '''
    line = []
    x0, y0 = coords_a
    x1, y1 = coords_b
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        line += [[x0, y0]]
        if x0 == x1 and y0 == y1:
            break
        e2 = err * 2
        if e2 > -dy:
            err = err - dy
            x0 = x0 + sx
        if e2 < dx:
            err = err + dx
            y0 = y0 + sy

    return line


def expand_path(path: List[Coords]) -> List[Coords]:
    '''
    Given a compressed path, return a new path that has all the segments
    in it interpolated.
    '''
    expanded = []
    if len(path) < 2:
        return expanded
    for i in range(len(path) - 1):
        expanded += bresenham(path[i], path[i + 1])
    expanded += [path[:-1]]
    return expanded


def smoothen_path(
    grid, path: List[Coords], use_raytrace=False
) -> List[Coords]:
    x0, y0 = path[0]

    sx, sy = path[0]
    new_path = [[sx, sy]]

    interpolate = raytrace if use_raytrace else bresenham
    last_valid = path[1]
    for coord in path[2:-1]:
        line = interpolate([sx, sy], coord)
        blocked = False
        for test_coord in line[1:]:
            if not grid.walkable(test_coord[0], test_coord[1]):
                blocked = True
                break
        if not blocked:
            new_path.append(last_valid)
            sx, sy = last_valid
        last_valid = coord

    new_path.append(path[-1])
    return new_path
