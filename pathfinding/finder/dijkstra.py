from .a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


class DijkstraFinder(AStarFinder):
    def __init__(self, weight=1, diagonal_movement=DiagonalMovement.never):
        def heuristic(dx, dy):
            return 0
        
        super(DijkstraFinder, self).__init__(
            weight=weight, diagonal_movement=diagonal_movement)
        
        self.heuristic = heuristic