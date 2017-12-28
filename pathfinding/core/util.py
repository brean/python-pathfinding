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


def bi_backtrace(node_a, node_b):
    """
    Backtrace from start and end node, returns the path for bi-directional A*
    (including both start and end nodes)
    """
    path_a = backtrace(node_a)
    path_b = backtrace(node_b)
    path_b.reverse()
    print(path_a + path_b)
    return path_a + path_b
