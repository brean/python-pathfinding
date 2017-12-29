import pandas
import numpy as np

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def _find(matrix):
    grid = Grid(matrix=matrix)
    print(matrix)

    start = grid.node(0, 0)
    end = grid.node(2, 4)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)

    print('operations:', runs, 'path length:', len(path))
    print(grid.grid_str(path=path, start=start, end=end))

    assert path == [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4)]
    assert len(path) == 7

def test_csv_pandas_str():
    """
    test to load a csv file using pandas (as string).
    """
    _find(np.array(pandas.io.parsers.read_csv("csv_file.csv")).astype("str"))

def test_csv_pandas_int():
    """
    test to load a csv file using pandas (as int).
    """
    _find(np.array(pandas.io.parsers.read_csv("csv_file.csv")).astype("int"))
