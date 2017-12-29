from .a_star import AStarFinder, MAX_RUNS, TIME_LIMIT
from pathfinding.core.diagonal_movement import DiagonalMovement


class DijkstraFinder(AStarFinder):
    def __init__(self, weight=1,
            diagonal_movement=DiagonalMovement.never,
            time_limit=TIME_LIMIT,
            max_runs=MAX_RUNS):
        self.time_limit = time_limit
        self.max_runs = max_runs

        def heuristic(dx, dy):
            # return 0, so node.h will always be calculated as 0,
            # distance cost (node.f) is calculated only from
            # start to current point (node.g)
            return 0

        super(DijkstraFinder, self).__init__(
            weight=weight, diagonal_movement=diagonal_movement)

        self.heuristic = heuristic
