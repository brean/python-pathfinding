from typing import Dict, List, Set
from .node import GraphNode


class Graph:
    def __init__(
            self, edges: List[Set] = None, nodes: Dict[int, GraphNode] = None,
            bi_directional: bool = False):
        # edges defined by node-from, node-to and its cost
        self.edges = edges if edges else []
        self.nodes = nodes if nodes else {}
        self.bi_directional = bi_directional
        # we will call cleanup automatically if dirty is True
        self.dirty = False
        self.edge_node_items()
        if not nodes:
            self.generate_nodes()

    def edge_node_items(self):
        for edge in self.edges:
            node = edge[0]
            if isinstance(node, (int, float, str)):
                if node in self.nodes:
                    edge[0] = self.nodes[node]
                else:
                    self.nodes[node] = GraphNode(node_id=node)
                    edge[0] = self.nodes[node]
            node = edge[1]
            if isinstance(edge[1], (int, float, str)):
                if node in self.nodes:
                    edge[1] = self.nodes[node]
                else:
                    self.nodes[node] = GraphNode(node_id=node)
                    edge[1] = self.nodes[node]

    def generate_nodes(self):
        for edge in self.edges:
            from_node, to_node, _ = edge
            self.nodes[from_node.node_id] = from_node
            self.nodes[to_node.node_id] = to_node

    def neighbors(self, node: GraphNode, **kwargs):
        nodes = [
            edge[1] for edge in self.edges
            if edge[0] == node]
        if self.bi_directional:
            nodes += [
                edge[0] for edge in self.edges
                if edge[1] == node]
        return nodes

    def calc_cost(self, node_a, node_b, _weighted=False):
        for edge in self.edges:
            if edge[0].node_id == node_a.node_id and \
                    edge[1].node_id == node_b.node_id:
                return edge[2]
            if self.bi_directional and \
                    edge[1].node_id == node_a.node_id and \
                    edge[0].node_id == node_b.node_id:
                return edge[2]
        raise RuntimeError('not connected')

    def node(self, node_id):
        return self.nodes[node_id]

    def cleanup(self):
        for node in self.nodes.values():
            node.cleanup()
