import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
from prettyprinting.baseprinter import _PrettyPrint


class PrettyPrintBDD(_PrettyPrint):
    """
    Pretty printer for BDDs.
    Prints the BDD in a tree like structure. Leafs are drawn as boxes
    containing either a zero or a one depending on their value. The other
    nodes are drawn as circles named by the basic event of it.
    A dashed line indicates the path taken if the basic event is False,
    a solid line indicates True.
    Uses networkx and pygraphviz.
    """

    def __init__(self, bdd, multi_edge_radians=0.2):
        """
        Constructor for a PrettyPrintBDD class.
        :param bdd: The BDD to print.
        """
        self.bdd = bdd
        self.graph = nx.MultiDiGraph()  # multiedges between nodes
        self.labels = dict()  # dictionary to store labels of nodes in
        self.multi_edge_radians = multi_edge_radians

    def _pretty_print(self):
        """
        The override for the _pretty_print function creates the graph and
        then draws it.
        """
        self._create_graph()
        self._draw_graph()

    def _create_graph(self):
        """
        Adds all the nodes to the networkx graph structure.
        To do this, the add nodes function is called with the full system.
        """
        self._add_nodes(self.bdd.get_system())

    def _add_nodes(self, node):
        """
        Adds the current node to the graph and recursively calls the same
        function for the children.
        Also assigns labels to the node names for later use.
        :param node: The node to add.
        """
        self.graph.add_node(node.get_unique_name())
        self.labels[node.get_unique_name()] = node.get_name()
        if node.has_children():
            for child, dashed in zip(
                    [node.get_true_node(), node.get_false_node()],
                    [False, True]):  # to check if the line is dashed
                self._add_nodes(child)
                self.graph.add_edge(node.get_unique_name(),
                                    child.get_unique_name(),
                                    dashed=dashed)

    def _draw_graph(self):
        """
        Draws the BDD graph. This is done by first drawing the nodes, then
        the edges and finally the labels.
        """
        pos = graphviz_layout(self.graph, prog='dot')
        nx.draw(self.graph, pos, node_size=0, edgelist=[])
        self._draw_nodes(pos)
        self._draw_edges(pos)
        self._draw_labels(pos)

    def _draw_nodes(self, pos):
        """
        Draw the nodes of the BDD graph.
        A distinction is made between leaf nodes and basic event nodes,
        the leaf nodes are drawn as boxes whereas the basic events are
        drawn as circles.
        :param pos: The positions of the nodes.
        """
        circles, boxes = [], []
        for node in self.graph.nodes:
            if node in [True, False]:
                boxes.append(node)
            else:
                circles.append(node)
        nx.draw_networkx_nodes(self.graph, pos, boxes, node_shape='s',
                               edgecolors='#000000', node_color='#ffffff')
        nx.draw_networkx_nodes(self.graph, pos, circles, node_shape='o',
                               node_color='#ffffff', edgecolors='#000000')

    def _get_edge_dashed(self, edge):
        """
        Return whether or not the given edge should be dashed.
        """
        return self.graph.get_edge_data(*edge)['dashed']

    def _get_edge_style(self, edge):
        """
        Return the style that the line representing the given edge should
        have.
        """
        if self._get_edge_dashed(edge):
            return 'dashed'
        else:
            return 'solid'

    def _edge_is_multiedge(self, edge):
        """
        Return whether or not the given edge is a multiedge (an edge that
        exists multiple times).
        """
        return len(self.graph[edge[0]][edge[1]]) > 1

    def _draw_edges(self, pos):
        """
        Draw the edges of the BDD graph.
        The arguments given to the draw_networkx_edges are built up over
        the duration of this function.
        We choose the relevant style (dashed or solid and if there are
        multiple edges between nodes we angle them so both of them are
        visible.
        :param pos: The positions of the nodes.
        """
        for edge in self.graph.edges:
            edge_data = {'arrows': True,
                         'arrowstyle': '-',
                         'style': self._get_edge_style(edge)}
            if self._edge_is_multiedge(edge):
                if self._get_edge_dashed(edge):
                    edge_data['connectionstyle'] = \
                        self._multiedge_style(True)
                else:
                    edge_data['connectionstyle'] = \
                        self._multiedge_style(False)
            nx.draw_networkx_edges(self.graph, pos, [edge], **edge_data)

    def _multiedge_style(self, negative):
        """
        Return the connectionstyle property for a multiedge in the drawn
        graph.
        :param negative: If the angle should be negative
        """
        if not negative:
            return 'arc3, rad={}'.format(self.multi_edge_radians)
        else:
            return 'arc3, rad=-{}'.format(self.multi_edge_radians)

    def _draw_labels(self, pos):
        """
        Draw the labels of the BDD graph.
        :param pos: The positions of the nodes.
        """
        nx.draw_networkx_labels(self.graph, pos, self.labels)
