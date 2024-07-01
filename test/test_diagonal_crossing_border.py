from pathfinding.core.grid import Grid, DiagonalMovement


def test_diagonal_crossing():
    grid = Grid(5, 5)
    grid.set_passable_left_right_border()
    nb = grid.neighbors(grid.node(4, 2), DiagonalMovement.always)
    neighbors = [(n.x, n.y) for n in nb]
    print(grid.grid_str(path=nb))
    assert set(neighbors) == set([
        (4, 1), (0, 2), (4, 3), (3, 2), 
        (3, 1), (3, 3), (0, 1), (0, 3)])
