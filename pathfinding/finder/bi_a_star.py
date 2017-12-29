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

    def find_path(self, start, end, grid):
        """
        find a path from start to end node on grid using the A* algorithm
        :param start: start node
        :param end: end node
        :param grid: grid that stores all possible steps/tiles as 2D-list
        :return:
        """
        self.start_time = time.time() # execution time limitation
        self.runs = 0 # count number of iterations

        start_open_list = []
        start.g = 0
        start.f = 0
        heapq.heappush(start_open_list, start)
        start.opened = BY_START

        end_open_list = []
        end.g = 0
        end.f = 0
        heapq.heappush(end_open_list, end)
        end.opened = BY_END

        while len(start_open_list) > 0 and len(end_open_list) > 0:
            self.runs += 1
            if not self.keep_running():
                break

            path = self.check_neighbors(start, end, grid, start_open_list,
                open_value=BY_START, backtrace_by=BY_END)
            if path:
                return path, self.runs

            path = self.check_neighbors(end, start, grid, end_open_list,
                open_value=BY_END, backtrace_by=BY_START)
            if path:
                return path, self.runs

        # failed to find path
        return [], self.runs
