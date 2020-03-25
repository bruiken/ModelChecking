from bdd.nodes import BasicEventNode


class BDDAnalyser:
    """
    The BDDAnalyser class is used to analyse BDDs.
    It can give you the number of nodes and edges in a BDD.
    """

    def __init__(self, bdd):
        """
        Constructor for a BDDAnalyser.
        It will also immediately analyse the graph, so results are ready
        after calling the constructor.
        :param bdd: The BDD to analyse.
        """
        self.bdd = bdd
        self.edges, self.nodes = self._analyse_graph()

    def _analyse_graph(self):
        """
        Analyses the given BDD.
        It will first decide how many nodes it has, then calculate how
        many edges it has.
        :return: A tuple containing the number of nodes and edges.
        """
        nodes = self._analyse_node(self.bdd.get_system(), set()) + 2
        edges = max(0, 2 * nodes - 4)
        return edges, nodes

    def _analyse_node(self, node, visited):
        """
        Analyses one node, this calculates how many nodes are below the
        current node. LeafNodes are not calculated. Instead, these are
        added after calling this function.
        :param node: The current node to analyse.
        :param visited: A set of already visited nodes.
        :return: The number of BasicEventNodes below and including the
                 current node.
        """
        if isinstance(node, BasicEventNode):
            if node in visited:
                return 0
            visited.add(node)
            true_c = self._analyse_node(node.get_true_node(), visited)
            false_c = self._analyse_node(node.get_false_node(), visited)
            return 1 + true_c + false_c
        return 0

    def number_edges(self):
        """
        Return the number of edges in the BDD.
        """
        return self.edges

    def number_nodes(self):
        """
        Return the number of nodes in the BDD.
        """
        return self.nodes
