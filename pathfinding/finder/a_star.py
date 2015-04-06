# -*- coding: utf-8 -*-
import heapq
import logging
from pathfinding.core.heuristic import manhatten
from pathfinding.core.util import backtrace


# max. amount of tries until we abort the search
MAX_RUNS = 0

# square root of 2
SQRT2 = 2 ** 0.5


class AStarFinder(object):
    def __init__(self, heuristic=None, weight=1):
        """
        find shortest path using A* algorithm
        :param heuristic: heuristic used to calculate distance of 2 points
        :param weight: weight for the edges
        :return:
        """
        if not heuristic:
            heuristic = manhatten
        self.heuristic = heuristic
        self.weight = weight

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
        open_list = []
        start.g = 0
        start.f = 0
        
        # push the start node into the open list
        heapq.heappush(open_list, start)
        runs = 0
        
        # while the open list is not empty
        while len(open_list) > 0:
            runs += 1
            if 0 < max_runs <= runs:
                logging.error('A* run into barrier of {} iterations without '
                              'finding the destination'.format(max_runs))
                break
            
            # pop node with minimum 'f' value
            node = heapq.nsmallest(1, open_list)[0]
            open_list.remove(node)
            node.closed = True
            
            # if reached the end position, construct the path and return it
            if node == end:
                return backtrace(end), runs

            # get neighbors of the current node
            neighbors = grid.neighbors(node)
            for neighbor in neighbors:
                if neighbor.closed:
                    continue

                x = neighbor.x
                y = neighbor.y

                # get the distance between current node and the neighbor
                ng = node.g
                if x - node.x == 0 or y - node.y == 0:
                    # direct neighbor - distance is 1
                    ng += 1
                else:
                    # not a direct neighbor - diagonal movement
                    ng += SQRT2
                    
                # check if the neighbor has not been inspected yet, or
                # can be reached with smaller cost from the current node
                if not neighbor.opened or ng < neighbor.g:
                    neighbor.g = ng
                    neighbor.h = neighbor.h or self.weight * \
                        self.heuristic(abs(x - end.x), abs(y - end.y))
                    # f is the estimated total cost from start to goal
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = node

                    if not neighbor.opened:
                        heapq.heappush(open_list, neighbor)
                        neighbor.opened = True
                    else:
                        # the neighbor can be reached with smaller cost.
                        # Since its f value has been updated, we have to
                        # update its position in the open list
                        open_list.remove(neighbor)
                        heapq.heappush(open_list, neighbor)
        # failed to find path
        return [], runs
