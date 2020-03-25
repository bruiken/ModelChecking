from bdd.nodes import BasicEventNode


class BDDAnalyser:
    def __init__(self, bdd):
        self.bdd = bdd
        self.edges, self.nodes = self._analyse_graph()

    def _analyse_graph(self):
        nodes = self._analyse_node(self.bdd.get_system(), set()) + 2
        edges = max(0, 2 * nodes - 4)
        return edges, nodes

    def _analyse_node(self, node, visited):
        if isinstance(node, BasicEventNode):
            if node in visited:
                return 0
            visited.add(node)
            true_c = self._analyse_node(node.get_true_node(), visited)
            false_c = self._analyse_node(node.get_false_node(), visited)
            return 1 + true_c + false_c
        return 0

    def number_edges(self):
        return self.edges

    def number_nodes(self):
        return self.nodes
