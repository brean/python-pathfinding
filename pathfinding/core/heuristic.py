import math
from .util import SQRT2


def null(dx, dy) -> float:
    """
    special heuristic for Dijkstra
    return 0, so node.h will always be calculated as 0,
    distance cost (node.f) is calculated only from
    start to current point (node.g)
    """
    return 0


def manhattan(dx, dy) -> float:
    """manhattan heuristics"""
    return dx + dy


def euclidean(dx, dy) -> float:
    """euclidean distance heuristics"""
    return math.sqrt(dx * dx + dy * dy)


def chebyshev(dx, dy) -> float:
    """ Chebyshev distance. """
    return max(dx, dy)


def octile(dx, dy) -> float:
    f = SQRT2 - 1
    if dx < dy:
        return f * dx + dy
    else:
        return f * dy + dx
