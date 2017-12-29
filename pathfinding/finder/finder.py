# -*- coding: utf-8 -*-
import math
import heapq # used for the so colled "open list" that stores known nodes
import logging
import time # for time limitation
from pathfinding.core.heuristic import manhatten, octile
from pathfinding.core.util import backtrace, bi_backtrace
from pathfinding.core.diagonal_movement import DiagonalMovement


# max. amount of tries we iterate until we abort the search
MAX_RUNS = float('inf')
# max. time after we until we abort the search (in seconds)
TIME_LIMIT = float('inf')

# square root of 2 for diagonal distance
SQRT2 = math.sqrt(2)

# used for backtrace of bi-directional A*
BY_START = 1
BY_END = 2
'''
the default finder
'''

class Finder(object):
    def __init__(self, heuristic=None, weight=1,
                 diagonal_movement=DiagonalMovement.never,
                 time_limit=TIME_LIMIT,
                 max_runs=MAX_RUNS):
        """
        find shortest path
        :param heuristic: heuristic used to calculate distance of 2 points
            (defaults to manhatten)
        :param weight: weight for the edges
        :param diagonal_movement: if diagonal movement is allowed
            (see enum in diagonal_movement)
        :param time_limit: max. runtime in seconds
        :param max_runs: max. amount of tries until we abort the search
            (optional, only if we enter huge grids and have time constrains)
            <=0 means there are no constrains and the code might run on any
            large map.
        """
        self.time_limit = time_limit
        self.max_runs = max_runs

        self.diagonal_movement = diagonal_movement
        self.weight = weight
        self.heuristic = heuristic


    def calc_cost(self, node_a, node_b):
        """
        get the distance between current node and the neighbor (cost)
        """
        ng = node_a.g
        if node_b.x - node_a.x == 0 or node_b.y - node_a.y == 0:
            # direct neighbor - distance is 1
            ng += 1
        else:
            # not a direct neighbor - diagonal movement
            ng += SQRT2
        return ng


    def apply_heuristic(self, node_a, node_b):
        """
        helper function to calculate heuristic
        """
        return self.heuristic(
            abs(node_a.x - node_b.x),
            abs(node_a.y - node_b.y))


    def keep_running(self):
        """
        check, if we run into time or iteration constrains.
        """
        if self.runs >= self.max_runs:
            logging.error('{} run into barrier of {} iterations without '
                          'finding the destination'.format(
                            self.__name__, self.max_runs))
            return False
        if time.time() - self.start_time >= self.time_limit:
            logging.error('{} took longer than {} '
                          'seconds, aborting!'.format(
                            self.__name__, self.time_limit))
            return False
        return True
