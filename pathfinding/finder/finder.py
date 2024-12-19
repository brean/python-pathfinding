import time  # for time limitation
from ..core.grid import Grid
from ..core.diagonal_movement import DiagonalMovement
from ..core.heap import SimpleHeap


# max. amount of tries we iterate until we abort the search
MAX_RUNS = float('inf')
# max. time after we until we abort the search (in seconds)
TIME_LIMIT = float('inf')

# used for backtrace of bi-directional A*
BY_START = 1
BY_END = 2


class ExecutionTimeException(Exception):
    """
    Exception that gets thrown when a certain time has been exceeded.
    """
    def __init__(self, message):
        super(ExecutionTimeException, self).__init__(message)


class ExecutionRunsException(Exception):
    """
    Exception that gets thrown when the number of max. runs has been reached.
    """
    def __init__(self, message):
        super(ExecutionRunsException, self).__init__(message)


class Finder:
    def __init__(self, heuristic=None, weight: int = 1,
                 diagonal_movement: int = DiagonalMovement.never,
                 weighted: bool = True,
                 time_limit: float = TIME_LIMIT,
                 max_runs: int = MAX_RUNS):
        """
        Find shortest path
        :param heuristic: heuristic used to calculate distance of 2 points
            (defaults to manhattan)
        :param weight: weight for the edges
        :param diagonal_movement: if diagonal movement is allowed
            (see enum in diagonal_movement)
        :param weighted: the algorithm supports weighted nodes
            (should be True for A* and Dijkstra)
        :param time_limit: max. runtime in seconds
        :param max_runs: max. amount of tries until we abort the search
            (optional, only if we enter huge grids and have time constrains)
            <=0 means there are no constrains and the code might run on any
            large map.
        """
        self.time_limit = time_limit
        self.max_runs = max_runs
        self.weighted = weighted

        self.diagonal_movement = diagonal_movement
        self.weight = weight
        self.heuristic = heuristic

        self.start_time = 0  # execution time limitation
        self.runs = 0  # count number of iterations

    def apply_heuristic(self, node_a, node_b, heuristic=None, graph=None):
        """
        Helper function to apply heuristic
        """
        if not heuristic:
            heuristic = self.heuristic

        dx = abs(node_a.x - node_b.x)
        dy = abs(node_a.y - node_b.y)

        if isinstance(graph, Grid):
            if graph.passable_left_right_border and dx > graph.width / 2:
                dx = graph.width - dx

            if graph.passable_up_down_border and dy > graph.height / 2:
                dy = graph.height - dy

            nh = heuristic(dx, dy)
            # in a weighted graph we also need to multiply the calculated
            # value with the minimum weight of the graph
            if self.weighted:
                nh *= graph.min_weight
            return nh
        else:
            return heuristic(dx, dy)

    def find_neighbors(self, grid, node, diagonal_movement=None):
        '''
        Find neighbor, same for Djikstra, A*, Bi-A*, IDA*
        '''
        if not diagonal_movement:
            diagonal_movement = self.diagonal_movement
        return grid.neighbors(node, diagonal_movement=diagonal_movement)

    def keep_running(self):
        """
        Check, if we run into time or iteration constrains.

        :returns: True if we keep running and False if we run into a constraint
        """
        if self.runs >= self.max_runs:
            raise ExecutionRunsException(
                '{} run into barrier of {} iterations without '
                'finding the destination'.format(
                    self.__class__.__name__, self.max_runs))

        if time.time() - self.start_time >= self.time_limit:
            raise ExecutionTimeException(
                '{} took longer than {} seconds, aborting!'.format(
                    self.__class__.__name__, self.time_limit))

    def process_node(
            self, graph, node, parent, end, open_list, open_value=True):
        '''
        We check if the given node is part of the path by calculating its
        cost and add or remove it from our path
        :param node: the node we like to test
            (the neighbor in A* or jump-node in JumpPointSearch)
        :param parent: the parent node (of the current node we like to test)
        :param end: the end point to calculate the cost of the path
        :param open_list: the list that keeps track of our current path
        :param open_value: needed if we like to set the open list to something
            else than True (used for bi-directional algorithms)

        '''
        # calculate cost from current node (parent) to the next node (neighbor)
        ng = parent.g + graph.calc_cost(parent, node, self.weighted)

        if not node.opened or ng < node.g:
            old_f = node.f
            node.g = ng
            node.h = node.h or self.apply_heuristic(node, end, graph=graph)
            # f is the estimated total cost from start to goal
            node.f = node.g + node.h
            node.parent = parent
            if not node.opened:
                open_list.push_node(node)
                node.opened = open_value
            else:
                # the node can be reached with smaller cost.
                # Since its f value has been updated, we have to
                # update its position in the open list
                open_list.remove_node(node, old_f)
                open_list.push_node(node)

    def check_neighbors(self, start, end, graph, open_list,
                        open_value=True, backtrace_by=None):
        """
        Find next path segment based on given node
        (or return path if we found the end)

        :param start: start node
        :param end: end node
        :param grid: grid that stores all possible steps/tiles as 2D-list
        :param open_list: stores nodes that will be processed next
        """
        raise NotImplementedError(
            'Please implement check_neighbors in your finder')

    def clean_grid(self, grid):
        """Clean the map if needed."""
        if grid.dirty:
            grid.cleanup()
        grid.dirty = True

    def find_path(self, start, end, grid):
        """
        Find a path from start to end node on grid by iterating over
        all neighbors of a node (see check_neighbors)
        :param start: start node
        :param end: end node
        :param grid: grid that stores all possible steps/tiles as 2D-list
        (can be a list of grids)
        :return:
        """
        self.clean_grid(grid)

        self.start_time = time.time()  # execution time limitation
        self.runs = 0  # count number of iterations
        start.opened = True

        open_list = SimpleHeap(start, grid)

        while len(open_list) > 0:
            self.runs += 1
            self.keep_running()

            path = self.check_neighbors(start, end, grid, open_list)
            if path:
                return path, self.runs

        # failed to find path
        return [], self.runs

    def __repr__(self):
        """
        Return a human readable representation
        """
        return f"<{self.__class__.__name__}" \
            f"diagonal_movement={self.diagonal_movement} >"
