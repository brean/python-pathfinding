# Example implementations using python-pathfinding

## Image Simple

Create a map from an image and run a path finding algorithm on it. Requires: `pip install pillow`.

You can run it with an input and output file like this:
```
cd examples/image-simple/
python3 image_pathfinding.py -i map.png -o out.png
```

----

## Image Weighted

Create a map from and image and run a path finding algorithm on it. Requires: `pip install pillow`.

It maps specific colors to their weights. Make sure to update the value-mapping for your custom input-maps!

You can run it with an input and output file like this:

```
cd examples/image-weighted/
python3 image_pathfinding.py -i map.png -o foo.png
```

To add some randomization to the weights - you can use the `-r` flag: `python3 image_pathfinding.py -i map.png -o out.png -r 0.5`

Note: The terrain-map was generated with OpenSimplex-noise via [this Python script](https://github.com/O-X-L/opensimplex).
