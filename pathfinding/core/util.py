# -*- coding: utf-8 -*-
def backtrace(node):
    """
    Backtrace according to the parent records and return the path.
    (including both start and end nodes)
    """
    path = [(node.x, node.y)]
    while node.parent:
        node = node.parent
        path.append((node.x, node.y))
    path.reverse()
    return path

