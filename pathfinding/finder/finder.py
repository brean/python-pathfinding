# -*- coding: utf-8 -*-
import heapq  # used for the so colled "open list" that stores known nodes
import time  # for time limitation
from pathfinding.core.util import SQRT2
from pathfinding.core.diagonal_movement import DiagonalMovement


# max. amount of tries we iterate until we abort the search
MAX_RUNS = float('inf')
# max. time after we until we abort the search (in seconds)
TIME_LIMIT = float('inf')

# used for backtrace of bi-directional A*
BY_START = 1
BY_END = 2


class ExecutionTimeException(Exception):
    def __init__(self, message):
        super(ExecutionTimeException, self).__init__(message)


class ExecutionRunsException(Exception):
    def __init__(self, message):
        super(ExecutionRunsException, self).__init__(message)


class Finder(object):
    def __init__(self, heuristic=None, weight=1,
                 diagonal_movement=DiagonalMovement.never,
                 weighted=True,
                 time_limit=TIME_LIMIT,
                 max_runs=MAX_RUNS):
        """
        find shortest path
        :param heuristic: heuristic used to calculate distance of 2 points
            (defaults to manhattan)
        :param weight: weight for the edges
        :param diagonal_movement: if diagonal movement is allowed
            (see enum in diagonal_movement)
        :param weighted: the algorithm supports weighted nodes
            (should be True for A* and Dijkstra)
        :param time_limit: max. runtime in seconds
        :param max_runs: max. amount of tries until we abort the search
            (optional, only if we enter huge grids and have time constrains)
            <=0 means there are no constrains and the code might run on any
            large map.
        """
        self.time_limit = time_limit
        self.max_runs = max_runs
        self.weighted = weighted

        self.diagonal_movement = diagonal_movement
        self.weight = weight
        self.heuristic = heuristic

    def calc_cost(self, node_a, node_b):
        """
        get the distance between current node and the neighbor (cost)
        """
        if node_b.x - node_a.x == 0 or node_b.y - node_a.y == 0:
            # direct neighbor - distance is 1
            ng = 1
        else:
            # not a direct neighbor - diagonal movement
            ng = SQRT2

        # weight for weighted algorithms
        if self.weighted:
            ng *= node_b.weight

        return node_a.g + ng

    def apply_heuristic(self, node_a, node_b, heuristic=None):
        """
        helper function to apply heuristic
        """
        if not heuristic:
            heuristic = self.heuristic
        return heuristic(
            abs(node_a.x - node_b.x),
            abs(node_a.y - node_b.y))

    def find_neighbors(self, grid, node, diagonal_movement=None):
        '''
        find neighbor, same for Djikstra, A*, Bi-A*, IDA*
        '''
        if not diagonal_movement:
            diagonal_movement = self.diagonal_movement
        return grid.neighbors(node, diagonal_movement=diagonal_movement)

    def keep_running(self):
        """
        check, if we run into time or iteration constrains.
        :returns: True if we keep running and False if we run into a constraint
        """
        if self.runs >= self.max_runs:
            raise ExecutionRunsException(
                '{} run into barrier of {} iterations without '
                'finding the destination'.format(
                    self.__class__.__name__, self.max_runs))

        if time.time() - self.start_time >= self.time_limit:
            raise ExecutionTimeException(
                '{} took longer than {} seconds, aborting!'.format(
                    self.__class__.__name__, self.time_limit))

    def process_node(self, node, parent, end, open_list, open_value=True):
        '''
        we check if the given node is path of the path by calculating its
        cost and add or remove it from our path
        :param node: the node we like to test
            (the neighbor in A* or jump-node in JumpPointSearch)
        :param parent: the parent node (the current node we like to test)
        :param end: the end point to calculate the cost of the path
        :param open_list: the list that keeps track of our current path
        :param open_value: needed if we like to set the open list to something
            else than True (used for bi-directional algorithms)

        '''
        # calculate cost from current node (parent) to the next node (neighbor)
        ng = self.calc_cost(parent, node)

        if not node.opened or ng < node.g:
            node.g = ng
            node.h = node.h or \
                self.apply_heuristic(node, end) * self.weight
            # f is the estimated total cost from start to goal
            node.f = node.g + node.h
            node.parent = parent

            if not node.opened:
                heapq.heappush(open_list, node)
                node.opened = open_value
            else:
                # the node can be reached with smaller cost.
                # Since its f value has been updated, we have to
                # update its position in the open list
                open_list.remove(node)
                heapq.heappush(open_list, node)

    def check_neighbors(self, start, end, grid, open_list,
                        open_value=True, backtrace_by=None):
        """
        find next path segment based on given node
        (or return path if we found the end)

        :param start: start node
        :param end: end node
        :param grid: grid that stores all possible steps/tiles as 2D-list
        :param open_list: stores nodes that will be processed next
        """
        raise NotImplementedError(
            'Please implement check_neighbors in your finder')

    def find_path(self, start, end, grid):
        """
        find a path from start to end node on grid by iterating over
        all neighbors of a node (see check_neighbors)
        :param start: start node
        :param end: end node
        :param grid: grid that stores all possible steps/tiles as 2D-list
        :return:
        """
        self.start_time = time.time()  # execution time limitation
        self.runs = 0  # count number of iterations
        start.opened = True

        open_list = [start]

        while len(open_list) > 0:
            self.runs += 1
            self.keep_running()

            path = self.check_neighbors(start, end, grid, open_list)
            if path:
                return path, self.runs

        # failed to find path
        return [], self.runs
