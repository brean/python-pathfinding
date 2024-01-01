from pathfinding.core.grid import Grid
from pathfinding.core.graph import Graph
from pathfinding.finder.dijkstra import DijkstraFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


DATA = [
    {
        'matrix': [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ],
        'expected_path_cost': 2 + 3 + 6 + 9
    },
    {
        'matrix': [
            [1, 2, 5],
            [4, 3, 8],
            [7, 7, 9]
        ],
        'expected_path_cost': 2 + 3 + 7 + 9
    },
    {
        'matrix': [
            [3, 1, 2, 5],
            [2, 5, 4, 1],
            [4, 2, 9, 6],
            [4, 3, 2, 4]
        ],
        'expected_path_cost': 1 + 5 + 2 + 3 + 2 + 4
    },
    {
        'matrix': [
            [3, 1, 2, 5],
            [2, 5, 3, 1],
            [4, 2, 1, 6],
            [1, 3, 2, 4]
        ],
        'expected_path_cost': 1 + 2 + 3 + 1 + 2 + 4
    },
    {
        'matrix': [
            [10, 5, 8, 3],
            [20, 7, 1, 12],
            [4, 9, 12, 21],
            [13, 14, 15, 16]
        ],
        'expected_path_cost': 5 + 7 + 1 + 12 + 15 + 16
    },
]

# https://adventofcode.com/2023/day/17
ADVENT = '''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''


def matrix_to_edges(matrix):
    h = len(matrix)
    w = len(matrix[0])
    edges = []
    for x in range(w-1):
        for y in range(h):
            for i in range(2):
                edges.append([
                    f'x{x}_y{y}_r{i}',
                    f'x{x+1}_y{y}_r{i+1}',
                    matrix[x+1][y]])
            for i in range(3):
                edges.append([
                    f'x{x}_y{y}_u{i}',
                    f'x{x+1}_y{y}_r0',
                    matrix[x+1][y]])
                edges.append([
                    f'x{x}_y{y}_d{i}',
                    f'x{x+1}_y{y}_r0',
                    matrix[x+1][y]])
    for x in range(w):
        for y in range(h-1):
            for i in range(2):
                edges.append([
                    f'x{x}_y{y}_d{i}',
                    f'x{x}_y{y+1}_d{i+1}',
                    matrix[x][y+1]])
            for i in range(3):
                edges.append([
                    f'x{x}_y{y}_r{i}',
                    f'x{x}_y{y+1}_d0',
                    matrix[x][y+1]])
                edges.append([
                    f'x{x}_y{y}_l{i}',
                    f'x{x}_y{y+1}_d0',
                    matrix[x][y+1]])
    for x in range(1, w):
        for y in range(h):
            for i in range(2):
                edges.append([
                    f'x{x}_y{y}_l{i}',
                    f'x{x-1}_y{y}_l{i+1}',
                    matrix[x-1][y]])
            for i in range(3):
                edges.append([
                    f'x{x}_y{y}_u{i}',
                    f'x{x-1}_y{y}_l0',
                    matrix[x-1][y]])
                edges.append([
                    f'x{x}_y{y}_d{i}',
                    f'x{x-1}_y{y}_l0',
                    matrix[x-1][y]])
    for x in range(w):
        for y in range(1, h):
            for i in range(2):
                edges.append([
                    f'x{x}_y{y}_u{i}',
                    f'x{x}_y{y-1}_u{i+1}',
                    matrix[x][y-1]])
            for i in range(3):
                edges.append([
                    f'x{x}_y{y}_r{i}',
                    f'x{x}_y{y-1}_u0',
                    matrix[x][y-1]])
                edges.append([
                    f'x{x}_y{y}_l{i}',
                    f'x{x}_y{y-1}_u0',
                    matrix[x][y-1]])

    edges.append(["start", 'x1_y0_r1', matrix[1][0]])
    edges.append(["start", 'x0_y1_d1', matrix[0][1]])
    edges.append([f'x{w-1}_y{h-1}_r0', "end", 0])
    edges.append([f'x{w-1}_y{h-1}_r1', "end", 0])
    edges.append([f'x{w-1}_y{h-1}_r2', "end", 0])
    edges.append([f'x{w-1}_y{h-1}_d0', "end", 0])
    edges.append([f'x{w-1}_y{h-1}_d1', "end", 0])
    edges.append([f'x{w-1}_y{h-1}_d2', "end", 0])
    return edges


def test_graph_weighted():
    for data in DATA:
        matrix = data['matrix']
        matrix = list(map(list, zip(*matrix)))
        edges = matrix_to_edges(matrix)
        graph = Graph(edges=edges, bi_directional=False)
        finder = DijkstraFinder(diagonal_movement=DiagonalMovement.never)
        path, _ = finder.find_path(
            graph.node("start"), graph.node("end"), graph)
        path_cost = sum([
            graph.calc_cost(path[i], path[i+1]) for i in range(len(path)-1)])
        assert path_cost == data['expected_path_cost']


def test_grid_weighted():
    for data in DATA:
        matrix = data['matrix']
        grid = Grid(matrix=matrix)
        finder = DijkstraFinder()
        end = grid.node(len(matrix) - 1, len(matrix[0]) - 1)
        path, _ = finder.find_path(grid.node(0, 0), end, grid)

        print(grid.grid_str(path=path, show_weight=True))
        print(path)
        print([
            grid.calc_cost(path[i], path[i+1], weighted=True)
            for i in range(len(path)-1)])
        path_cost = sum([
            grid.calc_cost(path[i], path[i+1], weighted=True)
            for i in range(len(path)-1)])

        assert path_cost == data['expected_path_cost']


def test_advent():
    # this spoilers "Advent of Code" day 17
    # https://adventofcode.com/2023/day/17
    data = ADVENT.split("\n")
    data = [[int(dd) for dd in d] for d in data]
    data = list(map(list, zip(*data)))
    edges = matrix_to_edges(data)
    graph = Graph(edges=edges, bi_directional=False)

    finder = DijkstraFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(
        graph.node("start"), graph.node("end"), graph)
    path_cost = sum([
        graph.calc_cost(path[i], path[i+1]) for i in range(len(path)-1)])
    print(path)
    print(path_cost)
    assert path_cost == 102