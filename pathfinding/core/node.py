# -*- coding: utf-8 -*-
class Node(object):
    """
    basic node, saves X and Y coordinates on some grid and determine if 
    it is walkable.
    """
    def __init__(self, x=0, y=0, walkable=True):
        # Coordinates
        self.x = x
        self.y = y

        # Whether this node can be walked through.
        self.walkable = walkable

        # values used in the finder
        self.h = 0.0
        self.g = 0.0
        self.f = 0.0
        self.opened = 0
        self.closed = False
        self.parent = None

    def __lt__(self, other):
        """
        nodes are sorted by f value (see a_star.py)

        :param other: compare Node
        :return:
        """
        return self.f < other.f