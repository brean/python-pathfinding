# -*- coding: utf-8 -*-
import os
import json
import pytest
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.dijkstra import DijkstraFinder
from pathfinding.finder.bi_a_star import BiAStarFinder
from pathfinding.finder.ida_star import IDAStarFinder
from pathfinding.finder.breadth_first import BreadthFirstFinder
from pathfinding.finder.finder import ExecutionRunsException
from pathfinding.finder.finder import ExecutionTimeException
from pathfinding.core.grid import Grid
from pathfinding.core.diagonal_movement import DiagonalMovement


BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# test scenarios from Pathfinding.JS
scenarios = os.path.join(BASE_PATH, 'path_test_scenarios.json')
data = json.load(open(scenarios, 'r'))
finders = [AStarFinder, BiAStarFinder, DijkstraFinder, IDAStarFinder,
           BreadthFirstFinder]
TIME_LIMIT = 10  # give it a 10 second limit.


def grid_from_scenario(scenario):
    grid = Grid(matrix=scenario['matrix'])
    start = grid.node(scenario['startX'], scenario['startY'])
    end = grid.node(scenario['endX'], scenario['endY'])
    return grid, start, end


def test_path():
    """
    test scenarios defined in json file
    """
    for scenario in data:
        for find in finders:
            grid, start, end = grid_from_scenario(scenario)
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
            grid, start, end = grid_from_scenario(scenario)
            finder = find(diagonal_movement=DiagonalMovement.always,
                          time_limit=TIME_LIMIT)
            path, runs = finder.find_path(start, end, grid)
            print(find.__name__, runs, len(path))
            print(grid.grid_str(path=path, start=start, end=end))
            print('path: {}'.format(path))
            assert len(path) == scenario['expectedDiagonalLength']


def test_max_runs():
    for find in finders:
        grid, start, end = grid_from_scenario(data[1])
        finder = find(diagonal_movement=DiagonalMovement.always,
                      time_limit=TIME_LIMIT, max_runs=3)
        with pytest.raises(ExecutionRunsException):
            path, runs = finder.find_path(start, end, grid)
            print('{} finishes after {} runs without exception'.format(
                find.__name__, finder.runs))
        msg = '{} needed to much iterations'.format(
            finder.__class__.__name__)
        assert(finder.runs <= 3), msg


def test_time():
    grid, start, end = grid_from_scenario(data[1])
    for find in finders:
        finder = find(diagonal_movement=DiagonalMovement.always,
                      time_limit=-.1)
        with pytest.raises(ExecutionTimeException):
            path, runs = finder.find_path(start, end, grid)
            print('{} finishes after {} runs without exception'.format(
                find.__name__, finder.runs))
        msg = '{} took to long'.format(finder.__class__.__name__)
        assert(finder.runs == 1), msg


if __name__ == '__main__':
    test_path()
    test_path_diagonal()
