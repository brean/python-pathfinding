from .a_star import AStarFinder, MAX_RUNS, TIME_LIMIT
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.heuristic import null


class DijkstraFinder(AStarFinder):
    def __init__(self, weight=1,
                 diagonal_movement=DiagonalMovement.never,
                 time_limit=TIME_LIMIT,
                 max_runs=MAX_RUNS):
        super(DijkstraFinder, self).__init__(
            heuristic=null,
            weight=weight,
            diagonal_movement=diagonal_movement,
            time_limit=time_limit,
            max_runs=max_runs)
