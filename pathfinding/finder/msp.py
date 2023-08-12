import heapq
import time
from collections import deque, namedtuple
from ..core import heuristic
from ..finder.finder import Finder


class MinimumSpanningTree(Finder):
    """
    Minimum Spanning Tree implementation by Brad Beattie
    (see https://github.com/brean/python-pathfinding/issues/18)

    The wikipedia page has a nice description about MSP:
    https://en.wikipedia.org/wiki/Minimum_spanning_tree
    """
    def __init__(self, *args, **kwargs):
        super(MinimumSpanningTree, self).__init__(*args, **kwargs)
        self.heuristic = heuristic.null

    def tree(self, grid, start):
        return list(self.itertree(grid, start))

    def itertree(self, grid, start):

        # Finder.process_node requires an end node, which we don't have.
        # The following value tricks the call to Finder.apply_heuristic.
        # Though maybe we want to generate a limited spanning tree that
        # trends in a certain direction? In which case we'd want a more
        # nuanced solution.
        end = namedtuple("FakeNode", ["x", "y"])(-1, -1)

        start.opened = True

        open_list = [start]

        while len(open_list) > 0:
            self.runs += 1
            self.keep_running()

            node = heapq.nsmallest(1, open_list)[0]
            open_list.remove(node)
            node.closed = True
            yield node

            neighbors = self.find_neighbors(grid, node)
            for neighbor in neighbors:
                if not neighbor.closed:
                    self.process_node(
                        grid, neighbor, node, end, open_list, open_value=True)

    def find_path(self, start, end, grid):
        self.start_time = time.time()  # execution time limitation
        self.runs = 0  # count number of iterations

        for node in self.itertree(grid, start):
            if node == end:
                path = deque()
                step = node
                while step.parent:
                    path.appendleft(step)
                    step = step.parent
                path.appendleft(step)
                return path, self.runs
        else:
            return [], self.runs
