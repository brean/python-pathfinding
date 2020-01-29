# -*- coding: utf-8 -*-
import time
from .finder import TIME_LIMIT, MAX_RUNS, BY_START, BY_END
from .a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


class BiAStarFinder(AStarFinder):
    """
    Similar to the default A* algorithm from a_star.
    """
    def __init__(self, heuristic=None, weight=1,
                 diagonal_movement=DiagonalMovement.never,
                 time_limit=TIME_LIMIT,
                 max_runs=MAX_RUNS):
        """
        find shortest path using Bi-A* algorithm
        :param heuristic: heuristic used to calculate distance of 2 points
            (defaults to manhattan)
        :param weight: weight for the edges
        :param diagonal_movement: if diagonal movement is allowed
            (see enum in diagonal_movement)
        :param time_limit: max. runtime in seconds
        :param max_runs: max. amount of tries until we abort the search
            (optional, only if we enter huge grids and have time constrains)
            <=0 means there are no constrains and the code might run on any
            large map.
        """
        super(BiAStarFinder, self).__init__(
            heuristic=heuristic,
            weight=weight,
            diagonal_movement=diagonal_movement,
            time_limit=time_limit,
            max_runs=max_runs)

        self.weighted = False

    def find_path(self, start, end, grid):
        """
        find a path from start to end node on grid using the A* algorithm
        :param start: start node
        :param end: end node
        :param grid: grid that stores all possible steps/tiles as 2D-list
        :return:
        """
        self.start_time = time.time()  # execution time limitation
        self.runs = 0  # count number of iterations

        start_open_list = [start]
        start.g = 0
        start.f = 0
        start.opened = BY_START

        end_open_list = [end]
        end.g = 0
        end.f = 0
        end.opened = BY_END

        while len(start_open_list) > 0 and len(end_open_list) > 0:
            self.runs += 1
            self.keep_running()
            path = self.check_neighbors(start, end, grid, start_open_list,
                                        open_value=BY_START,
                                        backtrace_by=BY_END)
            if path:
                return path, self.runs

            self.runs += 1
            self.keep_running()
            path = self.check_neighbors(end, start, grid, end_open_list,
                                        open_value=BY_END,
                                        backtrace_by=BY_START)
            if path:
                return path, self.runs

        # failed to find path
        return [], self.runs
