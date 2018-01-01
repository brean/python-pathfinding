# -*- coding: utf-8 -*-
import os
import json
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.dijkstra import DijkstraFinder
from pathfinding.finder.bi_a_star import BiAStarFinder
from pathfinding.finder.ida_star import IDAStarFinder
from pathfinding.finder.breadth_first import BreadthFirstFinder
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement


BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# test scenarios from Pathfinding.JS
scenarios = os.path.join(BASE_PATH, 'path_test_scenarios.json')
data = json.load(open(scenarios, 'r'))
finders = [AStarFinder, BiAStarFinder, DijkstraFinder, IDAStarFinder, \
           BreadthFirstFinder]

TIME_LIMIT = 10 # give it a 10 second limit.

def test_path():
    """
    test scenarios defined in json file
    """
    for scenario in data:
        for find in finders:
            grid = Grid(matrix=scenario['matrix'])
            start = grid.node(scenario['startX'], scenario['startY'])
            end = grid.node(scenario['endX'], scenario['endY'])
            finder = find(time_limit=TIME_LIMIT)
            path, runs = finder.find_path(start, end, grid)
            print(find.__name__)
            print(grid.grid_str(path=path, start=start, end=end))
            print('path: {}'.format(path))
            assert len(path) == scenario['expectedLength']


def test_path_diagonal():
    # test diagonal movement
    for scenario in data:
        for find in finders:
            grid = Grid(matrix=scenario['matrix'])
            start = grid.node(scenario['startX'], scenario['startY'])
            end = grid.node(scenario['endX'], scenario['endY'])
            finder = find(diagonal_movement=DiagonalMovement.always,
                time_limit=TIME_LIMIT)
            path, runs = finder.find_path(start, end, grid)
            print(find.__name__, runs, len(path))
            print(grid.grid_str(path=path, start=start, end=end))
            print('path: {}'.format(path))
            assert len(path) == scenario['expectedDiagonalLength']


if __name__ == '__main__':
    test_path()
    test_path_diagonal()
