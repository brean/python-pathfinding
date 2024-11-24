import numpy as np

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

BORDERLESS_GRID = """
xxx
xxx
"""

BORDER_GRID = """
+---+
|   |
|   |
+---+
"""

WALKED_GRID = """
+---+
|s# |
|xe |
+---+
"""

SIMPLE_MATRIX = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
]

SIMPLE_WALKED = """
+---+
|sx |
| #x|
|  e|
+---+
"""


def test_str():
    """
    test printing the grid
    """
    grid = Grid(height=2, width=3)
    assert grid.grid_str(border=False, empty_chr='x') == BORDERLESS_GRID[1:-1]
    assert grid.grid_str(border=True) == BORDER_GRID[1:-1]
    grid.nodes[0][1].walkable = False
    start = grid.nodes[0][0]
    end = grid.nodes[1][1]
    path = [(0, 1)]
    assert grid.grid_str(path, start, end) == WALKED_GRID[1:-1]


def test_empty():
    """
    special test for empty values
    """
    matrix = ()
    grid = Grid(matrix=matrix)
    assert grid.grid_str() == '++\n||\n++'

    matrix = np.array(matrix)
    grid = Grid(matrix=matrix)
    assert grid.grid_str() == '++\n||\n++'


def test_numpy():
    """
    test grid from numpy array
    """
    matrix = np.array(SIMPLE_MATRIX)
    grid = Grid(matrix=matrix)

    start = grid.node(0, 0)
    end = grid.node(2, 2)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)

    assert grid.grid_str(path, start, end) == SIMPLE_WALKED[1:-1]


if __name__ == '__main__':
    test_str()
