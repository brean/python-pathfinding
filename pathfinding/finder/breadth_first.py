from .finder import Finder, TIME_LIMIT, MAX_RUNS
from pathfinding.core.util import backtrace
from pathfinding.core.diagonal_movement import DiagonalMovement


class BreadthFirstFinder(Finder):
    def __init__(self, heuristic=None, weight=1,
                 diagonal_movement=DiagonalMovement.never,
                 time_limit=TIME_LIMIT,
                 max_runs=MAX_RUNS):
        super(BreadthFirstFinder, self).__init__(
            heuristic=heuristic,
            weight=weight,
            weighted=False,
            diagonal_movement=diagonal_movement,
            time_limit=time_limit,
            max_runs=max_runs)
        if not diagonal_movement:
            self.diagonalMovement = DiagonalMovement.never

    def check_neighbors(self, start, end, grid, open_list):
        node = open_list.pop(0)
        node.closed = True

        if node == end:
            return backtrace(end)

        neighbors = self.find_neighbors(grid, node)
        for neighbor in neighbors:
            if neighbor.closed or neighbor.opened:
                continue

            open_list.append(neighbor)
            neighbor.opened = True
            neighbor.parent = node
