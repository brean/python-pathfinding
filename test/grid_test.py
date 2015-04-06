# -*- coding: utf-8 -*-
from pathfinding.core.grid import Grid

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

if __name__ == '__main__':
    test_str()
