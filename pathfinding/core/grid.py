# -*- coding: utf-8 -*-
from .node import Node
from pathfinding.core.diagonal_movement import DiagonalMovement


def build_nodes(width, height, matrix=None):
    """
    create nodes according to grid size. If a matrix is given it
    will be used to determine what nodes are walkable
    :rtype : list
    """
    nodes = [None] * height
    if matrix:
        assert len(matrix) == height
        assert len(matrix[0]) == width
    for y in range(height):
        nodes[y] = [None] * width
        for x in range(width):
            walkable = True
            # 0, False, None will be walkable
            # while others will be un-walkable
            if matrix and matrix[y][x]:
                walkable = False
            nodes[y][x] = Node(x, y, walkable)
    return nodes


class Grid(object):
    def __init__(self, width=None, height=None, matrix=None):
        """
        a grid represents the map (as 2d-list of nodes).
        """
        if width or height:
            self.width = width
            self.height = height
        else:
            self.width = len(matrix[0])
            self.height = len(matrix)
        self.nodes = build_nodes(self.width, self.height, matrix)

    def node(self, x, y):
        """
        get node at position
        :param x: x pos
        :param y: y pos
        :return:
        """
        return self.nodes[y][x]

    def inside(self, x, y):
        """
        check, if field position is inside map
        :param x: x pos
        :param y: y pos
        :return:
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def walkable(self, x, y):
        """
        check, if the tile is inside grid and if it is set as walkable
        """
        return self.inside(x, y) and self.nodes[y][x].walkable

    def neighbors(self, node, diagonal_movement=DiagonalMovement.never):
        """
        get all neighbors of one node
        :param node: node
        """
        x = node.x
        y = node.y
        neighbors = []
        s0 = d0 = s1 = d1 = s2 = d2 = s3 = d3 = False

        # ↑
        if self.walkable(x, y - 1):
            neighbors.append(self.nodes[y - 1][x])
            s0 = True
        # →
        if self.walkable(x + 1, y):
            neighbors.append(self.nodes[y][x + 1])
            s1 = True
        # ↓
        if self.walkable(x, y + 1):
            neighbors.append(self.nodes[y + 1][x])
            s2 = True
        # ←
        if self.walkable(x - 1, y):
            neighbors.append(self.nodes[y][x - 1])
            s3 = True

        if diagonal_movement == DiagonalMovement.never:
            return neighbors

        if diagonal_movement == DiagonalMovement.only_when_no_obstacle:
            d0 = s3 and s0
            d1 = s0 and s1
            d2 = s1 and s2
            d3 = s2 and s3
        elif diagonal_movement == DiagonalMovement.if_at_most_one_obstacle:
            d0 = s3 or s0
            d1 = s0 or s1
            d2 = s1 or s2
            d3 = s2 or s3
        elif diagonal_movement == DiagonalMovement.always:
            d0 = d1 = d2 = d3 = True

        # ↖
        if d0 and self.walkable(x - 1, y - 1):
            neighbors.append(self.nodes[y - 1][x - 1])

        # ↗
        if d1 and self.walkable(x + 1, y - 1):
            neighbors.append(self.nodes[y - 1][x + 1])

        # ↘
        if d2 and self.walkable(x + 1, y + 1):
            neighbors.append(self.nodes[y + 1][x + 1])

        # ↙
        if d3 and self.walkable(x - 1, y + 1):
            neighbors.append(self.nodes[y + 1][x - 1])

        return neighbors

    def grid_str(self, path=None, start=None, end=None,
                 border=True, start_chr='s', end_chr='e',
                 path_chr='x', empty_chr=' ', block_chr='#'):
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
        :return:
        """
        data = ''
        if border:
            data = '+{}+'.format('-'*len(self.nodes[0]))
        for y in range(len(self.nodes)):
            line = ''
            for x in range(len(self.nodes[y])):
                node = self.nodes[y][x]
                if node == start:
                    line += start_chr
                elif node == end:
                    line += end_chr
                elif path and (node.x, node.y) in path:
                    line += path_chr
                elif node.walkable:
                    line += empty_chr  # empty field
                else:
                    line += block_chr  # blocked field
            if border:
                line = '|'+line+'|'
            if data:
                data += '\n'
            data += line
        if border:
            data += '\n+{}+'.format('-'*len(self.nodes[0]))
        return data