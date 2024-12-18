from .a_star import AStarFinder, MAX_RUNS, TIME_LIMIT
from ..core.diagonal_movement import DiagonalMovement
from ..core.heuristic import null


class DijkstraFinder(AStarFinder):
    """
    Find shortest path using the best-first Dijkstra path finding algorithm.
    """

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

    def apply_heuristic(self, node_a, node_b, heuristic=None, graph=None):
        """
        Helper function to apply heuristic
        
        returns 0 as Dijkstra is not using any heuristic (but A* is).
        """
        return 0
