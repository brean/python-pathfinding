from typing import List
from .diagonal_movement import DiagonalMovement
from .node import GridNode
from ..core.util import SQRT2
try:
    import numpy as np
    USE_NUMPY = True
except ImportError:
    USE_NUMPY = False


def build_nodes(
        width, height, matrix=None, inverse=False,
        grid_id=None) -> List[List[GridNode]]:
    """
    create nodes according to grid size. If a matrix is given it
    will be used to determine what nodes are walkable.
    """
    nodes = []
    use_matrix = (isinstance(matrix, (tuple, list))) or \
        (USE_NUMPY and isinstance(matrix, np.ndarray) and matrix.size > 0)

    min_weight = float("inf")
    for y in range(height):
        nodes.append([])
        for x in range(width):
            # 0, '0', False will be obstacles
            # all other values mark walkable cells.
            # you can use values bigger then 0 to assign a weight.
            # If inverse is False it changes
            # (1 and up becomes obstacle and 0 or everything negative marks a
            #  free cells)
            weight = float(matrix[y][x]) if use_matrix else 1
            walkable = weight <= 0.0 if inverse else weight > 0

            if walkable and weight < min_weight:
                min_weight = weight

            nodes[y].append(GridNode(
                x=x, y=y, walkable=walkable, weight=weight, grid_id=grid_id))

    return nodes, min_weight


class Grid:
    def __init__(
            self, width=0, height=0, matrix=None, grid_id=None,
            inverse=False):
        """
        a grid represents the map (as 2d-list of nodes).
        """
        self.width = width
        self.height = height
        # we will call cleanup automatically if dirty is True
        self.dirty = False
        self.passable_left_right_border = False
        self.passable_up_down_border = False
        if isinstance(matrix, (tuple, list)) or (
                USE_NUMPY and isinstance(matrix, np.ndarray) and (
                matrix.size > 0)):
            self.height = len(matrix)
            self.width = self.width = len(matrix[0]) if self.height > 0 else 0
        if self.width > 0 and self.height > 0:
            self.nodes, self._min_weight = build_nodes(
                self.width, self.height, matrix, inverse, grid_id)
        else:
            self.nodes = [[]]
            self._min_weight = float("inf")

    def set_passable_left_right_border(self):
        self.passable_left_right_border = True

    def set_passable_up_down_border(self):
        self.passable_up_down_border = True

    def node(self, x, y) -> GridNode:
        """
        get node at position
        :param x: x pos
        :param y: y pos
        :return:
        """
        return self.nodes[y][x]

    def inside(self, x, y) -> bool:
        """
        check, if field position is inside map
        :param x: x pos
        :param y: y pos
        :return:
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def walkable(self, x, y) -> bool:
        """
        check, if the tile is inside grid and if it is set as walkable
        """
        return self.inside(x, y) and self.nodes[y][x].walkable

    def calc_cost(self, node_a, node_b, weighted=False):
        """
        get the distance between current node and the neighbor (cost)
        """
        if node_b.x - node_a.x == 0 or node_b.y - node_a.y == 0:
            # direct neighbor - distance is 1
            ng = 1
        else:
            # not a direct neighbor - diagonal movement
            ng = SQRT2

        # weight for weighted algorithms
        if weighted:
            ng *= node_b.weight

        return ng

    def neighbors(
        self, node: GridNode,
        diagonal_movement: DiagonalMovement = DiagonalMovement.never
    ) -> List[GridNode]:
        """
        get all neighbors of one node
        :param node: node
        """
        x = node.x
        y = node.y
        neighbors = []
        north = nw = east = ne = south = se = west = sw = False

        # ↑
        if y == 0 and self.passable_up_down_border:
            north_y = self.height - 1
        else:
            north_y = y - 1

        if self.walkable(x, north_y):
            neighbors.append(self.nodes[north_y][x])
            north = True

        # →
        if x == self.width - 1 and self.passable_left_right_border:
            east_x = 0
        else:
            east_x = x + 1

        if self.walkable(east_x, y):
            neighbors.append(self.nodes[y][east_x])
            east = True

        # ↓
        if y == self.height - 1 and self.passable_up_down_border:
            south_y = 0
        else:
            south_y = y + 1
        if self.walkable(x, south_y):
            neighbors.append(self.nodes[south_y][x])
            south = True

        # ←
        if x == 0 and self.passable_left_right_border:
            west_x = self.width - 1
        else:
            west_x = x - 1
        if self.walkable(west_x, y):
            neighbors.append(self.nodes[y][west_x])
            west = True

        # check for connections to other grids
        if node.connections:
            neighbors.extend(node.connections)

        if diagonal_movement == DiagonalMovement.never:
            return neighbors

        if diagonal_movement == DiagonalMovement.only_when_no_obstacle:
            nw = north and west
            ne = north and east
            se = south and east
            sw = south and west
        elif diagonal_movement == DiagonalMovement.if_at_most_one_obstacle:
            nw = north or west
            ne = north or east
            se = south or east
            sw = south or west
        elif diagonal_movement == DiagonalMovement.always:
            nw = ne = se = sw = True

        # ↖
        if nw:
            if x == 0 and self.passable_left_right_border:
                nw_x = self.width - 1
            else:
                nw_x = x - 1
            if y == 0 and self.passable_up_down_border:
                nw_y = self.height - 1
            else:
                nw_y = y - 1
            if self.walkable(nw_x, nw_y):
                neighbors.append(self.nodes[nw_y][nw_x])

        # ↗
        if ne:
            if x == self.width - 1 and self.passable_left_right_border:
                ne_x = 0
            else:
                ne_x = x + 1
            if y == 0 and self.passable_up_down_border:
                ne_y = self.height - 1
            else:
                ne_y = y - 1
            if self.walkable(ne_x, ne_y):
                neighbors.append(self.nodes[ne_y][ne_x])

        # ↘
        if se:
            if x == self.width - 1 and self.passable_left_right_border:
                se_x = 0
            else:
                se_x = x + 1
            if y == self.height - 1 and self.passable_up_down_border:
                se_y = 0
            else:
                se_y = y + 1
            if self.walkable(se_x, se_y):
                neighbors.append(self.nodes[se_y][se_x])

        # ↙
        if sw:
            if x == 0 and self.passable_left_right_border:
                sw_x = self.width - 1
            else:
                sw_x = x - 1
            if y == self.height - 1 and self.passable_up_down_border:
                sw_y = 0
            else:
                sw_y = y + 1
            if self.walkable(sw_x, sw_y):
                neighbors.append(self.nodes[sw_y][sw_x])

        return neighbors

    def cleanup(self):
        for y_nodes in self.nodes:
            for node in y_nodes:
                node.cleanup()

    def grid_str(self, path=None, start=None, end=None,
                 border=True, start_chr='s', end_chr='e',
                 path_chr='x', empty_chr=' ', block_chr='#',
                 show_weight=False) -> str:
        """
        create a printable string from the grid using ASCII characters

        :param path: list of nodes that show the path
        :param start: start node
        :param end: end node
        :param border: create a border around the grid
        :param start_chr: character for the start (default "s")
        :param end_chr: character for the destination (default "e")
        :param path_chr: character to show the path (default "x")
        :param empty_chr: character for empty fields (default " ")
        :param block_chr: character for blocking elements (default "#")
        :param show_weight: instead of empty_chr show the cost of each empty
                            field (shows a + if the value of weight is > 10)
        :return:
        """
        # create a dict as lookup-table for the path by string for performance
        path_cache = {}
        if path:
            for node in path:
                is_gn = isinstance(node, GridNode)
                x, y = (node.x, node.y) if is_gn else node[:2]
                path_cache[f'{x}_{y}'] = True

        # create the output string
        data = ''
        if border:
            data = f'+{"-" * len(self.nodes[0])}+'
        for y, _ in enumerate(self.nodes):
            line = ''
            for x, _ in enumerate(self.nodes[y]):
                node = self.nodes[y][x]
                if node == start:
                    line += start_chr
                elif node == end:
                    line += end_chr
                elif path and (f'{x}_{y}' in path_cache):
                    line += path_chr
                elif node.walkable:
                    # empty field
                    if node.weight > 10:
                        weight = '+'  # weight bigger than 10
                    elif node.weight < 1 and node.weight > 0:
                        weight = '-'  # weight between 0 and 1
                    else:
                        weight = str(int(node.weight))
                    line += weight if show_weight else empty_chr
                else:
                    line += block_chr  # blocked field
            if border:
                line = f'|{line}|'
            if data:
                data += '\n'
            data += line
        if border:
            data += f'\n+{"-" * len(self.nodes[0])}+'
        return data

    def __repr__(self):
        """
        return a human readable representation
        """
        return f"<{self.__class__.__name__} " \
            f"width={self.width} height={self.height}>"

    @property
    def min_weight(self) -> float:
        return self._min_weight

    def update_node(self, x, y, *, weight=None, walkable=None):
        node = self.node(x, y)

        if weight is None:
            weight = node.weight

        if walkable is None:
            walkable = node.walkable

        if walkable:
            if weight <= 0:
                raise ValueError("Weight of a walkable node must be positive")
            if weight < self._min_weight:
                self._min_weight = weight

        node.weight = weight
        node.walkable = walkable
