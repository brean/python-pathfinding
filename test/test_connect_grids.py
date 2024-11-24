from pathfinding.core.grid import Grid
from pathfinding.core.world import World
from pathfinding.finder.a_star import AStarFinder


PATH = [
    # start in the top right on the lower level
    (2, 0, 0),
    # then move left
    (1, 0, 0),
    (0, 0, 0),
    # and down
    (0, 1, 0),
    (0, 2, 0),
    # and to the right
    (1, 2, 0),
    (2, 2, 0),
    # now we reached the elevator, move to other map
    (2, 2, 1),
    # and continue upwards, around the obstacles
    (2, 1, 1),
    (2, 0, 1),
    # now to the left until we reach our goal
    (1, 0, 1),
    (0, 0, 1)
]


def test_connect():
    level0 = [
        [1, 1, 1],
        [1, 0, 0],
        [1, 1, 1]
    ]
    level1 = [
        [1, 1, 1],
        [0, 0, 1],
        [1, 1, 1]
    ]
    # create Grid instances for both level
    grid0 = Grid(matrix=level0, grid_id=0)
    grid1 = Grid(matrix=level1, grid_id=1)

    grid0.node(2, 2).connect(grid1.node(2, 2))
    grid1.node(2, 2).connect(grid0.node(2, 2))

    # create world with both grids
    world = World({
        0: grid0,
        1: grid1
    })

    finder = AStarFinder()
    path, _ = finder.find_path(grid0.node(2, 0), grid1.node(0, 0), world)
    assert [tuple(p) for p in path] == PATH
