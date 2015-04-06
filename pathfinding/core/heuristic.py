# -*- coding: utf-8 -*-
import math


def manhatten(dx, dy):
    """manhatten heuristics"""
    return dx + dy


def euclidean(dx, dy):
    """euclidean distance heuristics"""
    return math.sqrt(dx * dx + dy * dy)


def chebyshev(dx, dy):
    """ Chebyshev distance. """
    return max(dx, dy)


def octile(dx, dy):
    f = (2 ** 0.5) - 1
    if dx < dy:
        return f * dx + dy
    else:
        return f * dy + dx