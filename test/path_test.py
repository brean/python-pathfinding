# -*- coding: utf-8 -*-
import os
import json
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.grid import Grid


BASE_PATH = os.path.abspath(os.path.dirname(__file__))

# test scenarios from Pathfinding.JS
scenarios = os.path.join(BASE_PATH, 'path_test_scenarios.json')
data = json.load(open(scenarios, 'r'))


def test_path():
    """
    test scenarios defined in json file
    """
    for scenario in data:
        grid = Grid(matrix=scenario['matrix'])
        start = grid.node(scenario['startX'], scenario['startY'])
        end = grid.node(scenario['endX'], scenario['endY'])
        finder = AStarFinder()
        path, runs = finder.find_path(start, end, grid)
        assert len(path) == scenario['expectedLength']
    

if __name__ == '__main__':
    test_path()
