from .bi_a_star import BiAStarFinder
from ..core.diagonal_movement import DiagonalMovement
from .finder import TIME_LIMIT, MAX_RUNS
from ..core.heuristic import null


class BiDijkstraFinder(BiAStarFinder):
    """
    Bi-directional Dijkstra's algorithm.

    It is similar to bi-directional A* but with a heuristic of zero.
    This means the search expands purely based on the lowest cost from the
    start and end points.
    """

    def __init__(
        self,
        weight=1,
        diagonal_movement=DiagonalMovement.never,
        time_limit=TIME_LIMIT,
        max_runs=MAX_RUNS,
    ):
        """
        :param weight: weight for the edges
        :param diagonal_movement: if diagonal movement is allowed
            (see enum in diagonal_movement)
        :param time_limit: max. runtime in seconds
        :param max_runs: max. amount of tries until we abort the search
        """
        super(BiDijkstraFinder, self).__init__(
            heuristic=null,
            weight=weight,
            diagonal_movement=diagonal_movement,
            time_limit=time_limit,
            max_runs=max_runs,
        )

    def apply_heuristic(self, node_a, node_b, heuristic=None, graph=None):
        return 0
