import json
import os

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.best_first import BestFirst
from pathfinding.finder.bi_a_star import BiAStarFinder
from pathfinding.finder.breadth_first import BreadthFirstFinder
from pathfinding.finder.dijkstra import DijkstraFinder
from pathfinding.finder.finder import ExecutionRunsException
from pathfinding.finder.finder import ExecutionTimeException
from pathfinding.finder.ida_star import IDAStarFinder
from pathfinding.finder.msp import MinimumSpanningTree

import pytest


BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# test scenarios from Pathfinding.JS
scenarios = os.path.join(BASE_PATH, 'path_test_scenarios.json')
data = json.load(open(scenarios, 'r'))
finders = [AStarFinder, BestFirst, BiAStarFinder, DijkstraFinder,
           IDAStarFinder, BreadthFirstFinder, MinimumSpanningTree]
TIME_LIMIT = 10  # give it a 10 second limit.


def grid_from_scenario(scenario):
    inverse = scenario['inverse'] if 'inverse' in scenario else True
    grid = Grid(matrix=scenario['matrix'], inverse=inverse)
    start = grid.node(scenario['startX'], scenario['startY'])
    end = grid.node(scenario['endX'], scenario['endY'])
    return grid, start, end


def test_path():
    """
    test scenarios defined in json file
    """
    for scenario in data:
        grid, start, end = grid_from_scenario(scenario)
        for find in finders:
            grid.cleanup()
            finder = find(time_limit=TIME_LIMIT)
            weighted = False
            if 'weighted' in scenario:
                weighted = scenario['weighted']
            if weighted and not finder.weighted:
                continue
            path, _ = finder.find_path(start, end, grid)
            print(find.__name__)
            print(grid.grid_str(path=path, start=start, end=end,
                                show_weight=weighted))
            print('path: {}'.format(path))
            assert len(path) == scenario['expectedLength']


def test_path_diagonal():
    # test diagonal movement
    for scenario in data:
        grid, start, end = grid_from_scenario(scenario)
        for find in finders:
            grid.cleanup()
            finder = find(diagonal_movement=DiagonalMovement.always,
                          time_limit=TIME_LIMIT)
            weighted = False
            if 'weighted' in scenario:
                weighted = scenario['weighted']
            print(dir(find))
            if weighted and not finder.weighted:
                continue

            path, runs = finder.find_path(start, end, grid)
            print(find.__name__, runs, len(path))
            print(grid.grid_str(path=path, start=start, end=end,
                                show_weight=weighted))
            print('path: {}'.format(path))
            assert len(path) == scenario['expectedDiagonalLength']


def test_max_runs():
    grid, start, end = grid_from_scenario(data[1])
    for find in finders:
        grid.cleanup()
        finder = find(diagonal_movement=DiagonalMovement.always,
                      time_limit=TIME_LIMIT, max_runs=3)
        with pytest.raises(ExecutionRunsException):
            path, runs = finder.find_path(start, end, grid)
            print('{} finishes after {} runs without exception'.format(
                find.__name__, runs))
            print('path: {}'.format(path))
        msg = '{} needed to much iterations'.format(
            finder.__class__.__name__)
        assert finder.runs <= 3, msg


def test_time():
    grid, start, end = grid_from_scenario(data[1])
    for find in finders:
        grid.cleanup()
        finder = find(diagonal_movement=DiagonalMovement.always,
                      time_limit=-.1)
        with pytest.raises(ExecutionTimeException):
            path, runs = finder.find_path(start, end, grid)
            print('{} finishes after {} runs without exception'.format(
                find.__name__, runs))
            print('path: {}'.format(path))
        msg = '{} took to long'.format(finder.__class__.__name__)
        assert finder.runs == 1, msg


if __name__ == '__main__':
    test_path()
    test_path_diagonal()
