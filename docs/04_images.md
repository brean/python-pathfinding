# Working with images as input
Because its easier to visualize maps as pictures and to manipulate you often want to work on images instead of providing the map as big array.

We use Pillow for this as it has a pretty straight-forward API.

We define the green pixel in the image as start and the red pixel as end. To have some variation and combat compression we define them as ranges above a certain threshold (although the png-image in our lossless compressed):

```python
def green(pixel: list) -> bool: 
    """Returns True if the pixel is green (the starting point)"""
    return pixel[RED] < 10 and pixel[GREEN] > 250 and pixel[BLUE] < 10


def red(pixel: list) -> bool:
    """Returns True if the pixel is red (the goal position)"""
    return pixel[RED] > 250 and pixel[GREEN] < 10 and pixel[BLUE] < 10
```

Pixel are defined as walkable grid cells if each of their color values is above 50, so a strong gray is enough to make it walkable:

```python
def pixel_walkable(pixel, x, y):
    """returns True if the pixel is walkable."""
    return any([p > 50 for p in pixel])  # darker pixel are not walkable
```

In the main loop we iterate over all pixel to find start and end and create a boolean matrix as input for our Grid:
```python
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
```
You can of course use another finder or use another digital_movement-strategy like `DiagonalMovement.always`.
