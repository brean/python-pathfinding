from .a_star import AStarFinder


class DijkstraFinder(AStarFinder):
    def __init__(self, weight=1):
        def heuristic(dx, dy):
            return 0
        
        super(DijkstraFinder, self).__init__(weight=weight)
        
        self.heuristic = heuristic