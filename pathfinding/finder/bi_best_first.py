from .bi_a_star import BiAStarFinder
from ..core.diagonal_movement import DiagonalMovement
from .finder import TIME_LIMIT, MAX_RUNS


class BiBestFirstFinder(BiAStarFinder):
    """
    Bi-directional Best-First-Search algorithm.
    It is essentially the same as bi-directional A* but with a high weight
    on the heuristic, making it a greedy search.
    """

    def __init__(
        self,
        heuristic=None,
        weight=1,
        diagonal_movement=DiagonalMovement.never,
        time_limit=TIME_LIMIT,
        max_runs=MAX_RUNS,
    ):
        """
        :param heuristic: heuristic used to calculate distance of 2 points
            (defaults to manhattan)
        :param weight: weight for the edges
        :param diagonal_movement: if diagonal movement is allowed
            (see enum in diagonal_movement)
        :param time_limit: max. runtime in seconds
        :param max_runs: max. amount of tries until we abort the search
        """
        super(BiBestFirstFinder, self).__init__(
            heuristic=heuristic,
            weight=weight,
            diagonal_movement=diagonal_movement,
            time_limit=time_limit,
            max_runs=max_runs,
        )

        self.weighted = False

    def apply_heuristic(self, node_a, node_b, heuristic=None, graph=None):
        return (
            super(BiBestFirstFinder, self).apply_heuristic(
                node_a, node_b, heuristic, graph=graph
            )
            * 1000000
        )
