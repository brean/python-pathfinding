# -*- coding: utf-8 -*-
import heapq # used for the so colled "open list" that stores known nodes
import logging
from pathfinding.core.heuristic import manhatten, octile
from pathfinding.core.diagonal_movement import DiagonalMovement
from .a_star import *

class BiAStarFinder(AStarFinder):
    """
    Similar to the default A* algorithm from a_star.
    """

    def find_path(self, start, end, grid, max_runs=MAX_RUNS):
        """
        find a path from start to end node on grid using the A* algorithm
        :param start: start node
        :param end: end node
        :param grid: grid that stores all possible steps/tiles as 2D-list
        :param max_runs: max. amount of tries until we abort the search
            (optional, only if we enter huge grids and have time constrains)
            <=0 means there are no constrains and the code might run on any
            large map.
        :return:
        """
        start_open_list = []
        end_open_list = []
        start.g = 0
        start.f = 0
        heapq.heappush(start_open_list, start)
        start.opened = BY_START

        end.g = 0
        end.f = 0
        heapq.heappush(end_open_list, end)
        end.opened = BY_END

        runs = 0 # count number of iterations
        while len(start_open_list) > 0 and len(end_open_list) > 0:
            runs += 1
            if 0 < max_runs <= runs:
                logging.error('Bi-Directional A* run into barrier of {} '
                              'iterations without finding the '
                              'destination'.format(max_runs))
                break

            path = self.check_neighbors(start, end, grid, start_open_list,
                open_value=BY_START, backtrace_by=BY_END)
            if path:
                return path, runs

            path = self.check_neighbors(end, start, grid, end_open_list,
                open_value=BY_END, backtrace_by=BY_START)
            if path:
                return path, runs

        # failed to find path
        return [], runs
