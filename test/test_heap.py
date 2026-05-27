from pathfinding.core.heap import SimpleHeap
from pathfinding.core.grid import Grid


def test_heap():
    grid = Grid(width=10, height=10)
    start = grid.node(0, 0)
    open_list = SimpleHeap(start, grid)

    # Test pop
    assert open_list.pop_node() == start
    assert len(open_list) == 0

    # Test push
    open_list.push_node(grid.node(1, 1))
    open_list.push_node(grid.node(1, 2))
    open_list.push_node(grid.node(1, 3))

    assert open_list.pop_node() == grid.node(1, 1)
    assert open_list.pop_node() == grid.node(1, 2)
    assert open_list.pop_node() == grid.node(1, 3)
    assert len(open_list) == 0

    # Test inconsistent f
    test_node = grid.node(1,1)
    test_node.f = 1
    open_list.push_node(test_node)
    test_node.f = 0
    open_list.push_node(test_node)
    assert open_list.pop_node() == test_node
    assert open_list.pop_node() is None
    assert len(open_list) == 0
