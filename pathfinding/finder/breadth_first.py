from .finder import Finder, MAX_RUNS, TIME_LIMIT
from ..core.diagonal_movement import DiagonalMovement
from ..core.util import backtrace


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
