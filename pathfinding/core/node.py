import dataclasses


@dataclasses.dataclass
class Node:
    def __post_init__(self):
        # values used in the finder
        self.cleanup()

    def __lt__(self, other):
        """
        nodes are sorted by f value (see a_star.py)

        :param other: compare Node
        :return:
        """
        return self.f < other.f

    def cleanup(self):
        """
        reset all calculated values, fresh start for pathfinding
        """
        # cost from this node to the goal (for A* including the heuristic)
        self.h = 0.0

        # cost from the start node to this node
        # (calculated by distance function, e.g. including diagonal movement)
        self.g = 0.0

        # overall cost for a path using this node (f = g + h )
        self.f = 0.0

        self.opened = 0
        self.closed = False

        # used for backtracking to the start point
        self.parent = None

        # used for recurion tracking of IDA*
        self.retain_count = 0
        # used for IDA* and Jump-Point-Search
        self.tested = False


@dataclasses.dataclass
class GraphNode(Node):
    """
    simple node in a graph that's not a grid.
    """
    # id of the node in the graph
    node_id = str | int

    def __init__(self, node_id):
        self.node_id = node_id
        self.__post_init__()

    def __eq__(self, o):
        if isinstance(o, (int, str)):
            return o == self.node_id
        return self.node_id == o.node_id


@dataclasses.dataclass
class GridNode(Node):
    """
    basic node, saves X and Y coordinates on some grid and determine if
    it is walkable.
    """
    # Coordinates
    x: int = 0
    y: int = 0

    # Wether this node can be walked through.
    walkable: bool = True

    # used for weighted algorithms
    weight: float = 1.0

    # grid_id is used if we have more than one grid,
    # normally we just count our grids by number
    # but you can also use a string here.
    # Set it to None if you only have one grid.
    grid_id: int = None

    connections: list = None

    def __iter__(self):
        yield self.x
        yield self.y
        if self.grid_id is not None:
            yield self.grid_id

    def connect(self, other_node):
        if not self.connections:
            self.connections = [other_node]
        else:
            self.connections.append(other_node)
