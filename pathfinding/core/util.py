# -*- coding: utf-8 -*-
import math

# square root of 2 for diagonal distance
SQRT2 = math.sqrt(2)

def backtrace(node):
    """
    Backtrace according to the parent records and return the path.
    (including both start and end nodes)
    """
    path = [(node.x, node.y)]
    while node.parent:
        node = node.parent
        path.append((node.x, node.y))
    path.reverse()
    return path


def bi_backtrace(node_a, node_b):
    """
    Backtrace from start and end node, returns the path for bi-directional A*
    (including both start and end nodes)
    """
    path_a = backtrace(node_a)
    path_b = backtrace(node_b)
    path_b.reverse()
    return path_a + path_b


def interpolate(coords_a, coords_b):
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
        line += [(x0, y0)]
        if coords_a.x == coords_b.x and coords_a.y == coords_b.y:
            break
        e2 = err * 2
        if e2 > -dy:
            err = err - dy
            x0 = x0 + sx
        if e2 < dx:
            err = err + dx
            y0 = y0 + sy

    return line


def expand_path(path):
    '''
    Given a compressed path, return a new path that has all the segments
    in it interpolated.
    '''
    expanded = []
    if len(path) < 2:
        return expanded
    for i in range(len(path)-1):
        expanded += interpolate(path[i], path[i + 1])
    expanded += [path[:-1]]
    return expanded
