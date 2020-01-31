from .a_star import AStarFinder, MAX_RUNS, TIME_LIMIT
from pathfinding.core.diagonal_movement import DiagonalMovement


class BestFirst(AStarFinder):
    """
    Similar to the default A* algorithm from a_star.
    """
    def __init__(self, heuristic=None, weight=1,
                 diagonal_movement=DiagonalMovement.never,
                 time_limit=TIME_LIMIT,
                 max_runs=MAX_RUNS):
        """
        find shortest path using BestFirst algorithm
        :param heuristic: heuristic used to calculate distance of 2 points
            (defaults to manhattan)
        :param weight: weight for the edges
        :param diagonal_movement: if diagonal movement is allowed
            (see enum in diagonal_movement)
        :param time_limit: max. runtime in seconds
        :param max_runs: max. amount of tries until we abort the search
            (optional, only if we enter huge grids and have time constrains)
            <=0 means there are no constrains and the code might run on any
            large map.
        """
        super(BestFirst, self).__init__(
            heuristic=heuristic,
            weight=weight,
            diagonal_movement=diagonal_movement,
            time_limit=time_limit,
            max_runs=max_runs)

        self.weighted = False

    def apply_heuristic(self, node_a, node_b, heuristic=None):
        return super(BestFirst, self).apply_heuristic(
            node_a, node_b, heuristic) * 1000000
