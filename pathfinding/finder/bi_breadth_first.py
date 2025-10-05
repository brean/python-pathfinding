import time
from collections import deque

from .finder import BY_END, BY_START, Finder, MAX_RUNS, TIME_LIMIT
from ..core.diagonal_movement import DiagonalMovement
from ..core.util import bi_backtrace


class BiBreadthFirstFinder(Finder):
    """
    Bidirectional Breadth-First-Search (Bi-BFS)
    """

    def __init__(
        self,
        diagonal_movement=DiagonalMovement.never,
        time_limit=TIME_LIMIT,
        max_runs=MAX_RUNS,
    ):
        super(BiBreadthFirstFinder, self).__init__(
            weighted=False,
            diagonal_movement=diagonal_movement,
            time_limit=time_limit,
            max_runs=max_runs,
        )

    def _search_level(self, grid, queue, opened_by, looking_for):
        """
        Search one level from the given queue.
        """
        level_size = len(queue)
        for _ in range(level_size):
            self.runs += 1
            self.keep_running()

            node = queue.popleft()
            node.closed = True

            neighbors = self.find_neighbors(grid, node)
            for neighbor in neighbors:
                if neighbor.opened == opened_by:
                    continue
                if neighbor.opened == looking_for:
                    if opened_by == BY_START:
                        return bi_backtrace(node, neighbor)
                    else:
                        return bi_backtrace(neighbor, node)

                neighbor.opened = opened_by
                neighbor.parent = node
                queue.append(neighbor)
        return None

    def find_path(self, start, end, grid):
        """
        Find a path from start to end node on grid using Bi-BFS
        :param start: start node
        :param end: end node
        :param grid: grid that stores all possible nodes
        :return:
        """
        self.clean_grid(grid)

        self.start_time = time.time()
        self.runs = 0

        start_queue = deque([start])
        start.opened = BY_START
        start.parent = None

        end_queue = deque([end])
        end.opened = BY_END
        end.parent = None

        while start_queue and end_queue:
            path = self._search_level(grid, start_queue, BY_START, BY_END)
            if path:
                return path, self.runs

            path = self._search_level(grid, end_queue, BY_END, BY_START)
            if path:
                return path, self.runs

        # failed to find path
        return [], self.runs
