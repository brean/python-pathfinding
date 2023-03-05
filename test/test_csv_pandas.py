import os
import numpy as np
import pandas

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(BASE_PATH, 'csv_file.csv')


def _find(matrix):
    grid = Grid(matrix=matrix)
    print(matrix)

    start = grid.node(0, 0)
    end = grid.node(2, 4)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)

    print('operations:', runs, 'path length:', len(path))
    print(grid.grid_str(path=path, start=start, end=end))

    assert [tuple(p) for p in path] ==\
        [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4)]


def test_csv_pandas_str():
    """
    test to load a csv file using pandas (as string).
    """
    _find(np.array(pandas.io.parsers.read_csv(CSV_FILE)).astype("str"))


def test_csv_pandas_int():
    """
    test to load a csv file using pandas (as int).
    """
    _find(np.array(pandas.io.parsers.read_csv(CSV_FILE)).astype("int"))
