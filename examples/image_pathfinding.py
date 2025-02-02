# Create a Map from an image
import os
from pathlib import Path
import argparse

# Pillow
from PIL import Image

# pathfinding
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


# image file with the map
BASE_PATH = Path(os.path.dirname(__file__))
MAP_FILE = BASE_PATH / "map.png"
OUT_FILE = BASE_PATH / "out.png"
# color channel order, defaults to RGB
RED, GREEN, BLUE = 0, 1, 2


def green(pixel: list) -> bool: 
    """Returns True if the pixel is green (the starting point)"""
    return pixel[RED] < 10 and pixel[GREEN] > 250 and pixel[BLUE] < 10


def red(pixel: list) -> bool:
    """Returns True if the pixel is red (the goal position)"""
    return pixel[RED] > 250 and pixel[GREEN] < 10 and pixel[BLUE] < 10


def pixel_walkable(pixel, x, y):
    """returns True if the pixel is walkable."""
    return any([p > 50 for p in pixel])  # darker pixel are not walkable


def main(filename_map: str = MAP_FILE, filename_out: str = OUT_FILE):
    nodes = []
    if not Path(filename_map).exists():
        print(f'File {filename_map} does not exist.')
        return
    with Image.open(filename_map) as im:
        width, height = im.size
        for y in range(height):
            nodes.append([])
            for x in range(width):
                pixel = im.getpixel((x, y))
                node = pixel_walkable(pixel[:3], x, y)
                nodes[y].append(node)
                if red(pixel):
                    _goal = (x, y)
                if green(pixel):
                    _start = (x, y)
        grid = Grid(matrix=nodes)
        end = grid.node(*_goal)
        start = grid.node(*_start)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)

        # print(grid.grid_str(path=path, end=end, start=start))
        print('iterations:', runs, 'path length:', len(path))
        out = im.copy()
        for p in path[1:-1]:
            out.putpixel((p.x, p.y), (255, 165, 0))
        out.save(filename_out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='image_pathfinding',
        description='find a path in an image from a green pixel to a red one')
    parser.add_argument(
        '-i', '--filename_map',
        help='input file',
        default=MAP_FILE)
    parser.add_argument(
        '-o', '--filename_out',
        help='output file',
        default=OUT_FILE)

    main(**vars(parser.parse_args()))
