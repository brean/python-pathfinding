from pathfinding.core.grid import Grid
from pathfinding.finder.ida_star import IDAStarFinder


def test_unreachable_goal_returns_empty_path():
    # (1, 0) is an obstacle, so (2, 0) cannot be reached from (0, 0): there
    # is no diagonal movement by default and no other row to go around it
    # through. time_limit is a safety net for this test only, in case the
    # fix this guards is ever lost again: find_path() itself defaults to no
    # time or run limit (see issue #92).
    grid = Grid(matrix=[[1, 0, 1]])
    start = grid.node(0, 0)
    end = grid.node(2, 0)
    finder = IDAStarFinder(time_limit=10)

    path, runs = finder.find_path(start, end, grid)

    assert path == []
