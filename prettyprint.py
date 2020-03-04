import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from networkx.drawing.nx_agraph import graphviz_layout


class _PrettyPrint:
    """
    Base class for pretty printers.
    Pretty printers must override the _pretty_print function.
    """

    def _pretty_print(self):
        """
        The pretty print function must be overriden and sets up the pretty
        printing. The pretty printing should be done in matplotlib such
        that savefig and show can be called on it.
        """
        pass

    def print_to_file(self, filename, dpi=None):
        """
        Prints the current figure to a file.
        :param filename: The filename.
        :param dpi: The DPI of the drawing.
        """
        self._pretty_print()
        plt.savefig(filename, dpi=dpi)

    def print_to_window(self):
        """
        Prints the current figure to a window.
        """
        self._pretty_print()
        plt.show()


class PrettyPrintFaultTree(_PrettyPrint):
    """
    Pretty printer for fault trees.
    Prints the fault tree in a tree like structure, uses the images
    defined in the FaultTree class to display the gates. Basic events are
    drawn as regular nodes.
    The edges and base events are colored according to their state.
    The nodes are labelled with their name.
    Uses networkx and pygraphviz.
    """

    def __init__(self, fault_tree, image_size=0.1, font_size=13):
        """
        Constructor for a PrettyPrintFaultTree class.
        :param fault_tree: The fault tree to be printed.
        :param image_size: The image size (for the gates).
        :param font_size: Font size for the labels.
        """
        self.fault_tree = fault_tree
        self.graph = nx.DiGraph()  # using a DirectedGraph for a tree
        self.image_size = image_size
        self.font_size = font_size

    def _pretty_print(self):
        """
        Pretty print for the fault trees calls the create graph function.
        After that the graph is drawn using the draw graph function.
        """
        self._create_graph()
        self._draw_graph()

    def _create_graph(self):
        """
        Adds all the gates to the networkx graph structure.
        To do this, the add nodes function is called with the full system.
        """
        self._add_nodes(self.fault_tree.get_system())

    def _add_nodes(self, gate):
        """
        Adds a node for the given gate and recursively calls the function
        on all the input gates of it.
        Then it also creates edges from the gate to the child gates.
        The other way around would make more sense but then the tree gets
        printed upside down.
        :param gate: The gate to add to the graph.
        """
        self.graph.add_node(gate.get_unique_index())
        for child_gate in gate.get_input_gates():
            self._add_nodes(child_gate)
            self.graph.add_edge(
                gate.get_unique_index(),
                child_gate.get_unique_index()
            )

    def _draw_graph(self):
        """
        Draw graph draws the entire graph. This is done by first drawing
        the edges, then the labels and finally the nodes.
        Even though all the parts are drawn seperately, we still call the
        draw function on the entire graph to force a plot with the correct
        size.
        The positions for all the nodes are calculated using
        graphviz_layout.
        """
        pos = graphviz_layout(self.graph, prog='dot')
        nx.draw(self.graph, pos, node_size=0, edgelist=[])
        self._draw_edges(pos)
        self._draw_labels(pos)
        self._draw_nodes(pos)

    def _draw_edges(self, pos):
        """
        Draws the edges of the graph.
        It first splits up the edges in edges which are on and off, then
        draws them with either green or red respectively.
        :param pos: The positions for all the nodes.
        """
        edges_on, edges_off = [], []
        for source, dest in self.graph.edges():
            if self.fault_tree.get_gate(dest).apply(False):
                edges_on.append((source, dest))
            else:
                edges_off.append((source, dest))
        nx.draw_networkx_edges(self.graph, pos, edges_on, edge_color='g',
                               width=3, arrows=False)
        nx.draw_networkx_edges(self.graph, pos, edges_off, edge_color='r',
                               width=3, arrows=False)

    def _draw_labels(self, pos):
        """
        Draws the labels for the nodes. For this a new Axes object is
        created. This axes has a high Z-order so it is drawn on top of the
        graph.
        :param pos: The positions for all the nodes.
        """
        label_axis = plt.Axes(plt.gcf(), [0, 0, 1, 1])
        label_axis.set_axis_off()
        label_axis.set_zorder(10)
        plt.gcf().add_axes(label_axis)
        for node in self.graph.nodes:
            name = self.fault_tree.get_gate(node).get_name()
            label_axis.text(*pos[node], name, ha='center', va='center',
                            transform=label_axis.transData, weight='bold',
                            color=(.3, .3, .3), fontsize=self.font_size)

    def _draw_nodes(self, pos):
        """
        Draw the nodes of the graph.
        This is done in three steps: the basic events, the non-basic
        events and finally the images of the gates.
        :param pos: The positions for all the nodes.
        """
        self._draw_basic_events(pos)
        self._draw_non_basic_gates(pos)
        self._draw_node_images(pos)

    def _draw_basic_events(self, pos):
        """
        Draws the basic events of the graph.
        They are first split up based on their state. Then drawn in green
        or red if they are on or off.
        :param pos: The positions for all the nodes.
        """
        nodes_on, nodes_off = [], []
        for basic_event in self.fault_tree.get_basic_events().values():
            if self.fault_tree.get_gate(basic_event.get_unique_index()):
                if basic_event.get_state():
                    nodes_on.append(basic_event.get_unique_index())
                else:
                    nodes_off.append(basic_event.get_unique_index())
        nx.draw_networkx_nodes(self.graph, pos, nodes_on, node_color='g')
        nx.draw_networkx_nodes(self.graph, pos, nodes_off, node_color='r')

    def _draw_non_basic_gates(self, pos):
        """
        Draws all the non-basic events.
        The nodes are drawn with a size of 0 since we use images to
        represent them.
        :param pos: The positions for all the nodes.
        """
        basic_events = list(map(
            lambda x: x.get_unique_index(),
            self.fault_tree.get_basic_events().values()
        ))
        nodes = []
        for node in self.graph.nodes:
            if node not in basic_events:
                nodes.append(node)
        nx.draw_networkx_nodes(self.graph, pos, nodes, node_size=0)

    def _draw_node_images(self, pos):
        """
        Draws the images for the gates (that have an image path).
        :param pos: The positions for all the nodes.
        """
        ax = plt.gca()
        for node in self.graph.nodes:
            img = self.fault_tree.get_gate(node).get_image_path()
            if img:
                self._draw_node_image(node, img, pos, ax)

    def _draw_node_image(self, node, img, pos, ax):
        """
        Draws the node image for a certain node.
        :param node: The node to draw the image on.
        :param img: The path to the image to draw.
        :param pos: The positions for all the nodes.
        :param ax: The axes to draw the images on.
        """
        x, y = self._transform_coords(pos[node], ax)
        a = plt.axes([x - self.image_size / 2., y - self.image_size / 2.,
                      self.image_size, self.image_size])
        a.axis('off')
        a.imshow(mpimg.imread(img))

    @staticmethod
    def _transform_coords(coordinates, ax):
        """
        Transforms coordinates of the node positions to coordinates
        relative on the screen ([0, 1]).
        :param coordinates: The coordinates to transform.
        :param ax: The axis to transform from.
        :return: the transformed coordinates.
        """
        ax_trans = ax.transData.transform
        fig_trans = plt.gcf().transFigure.inverted().transform
        return fig_trans(ax_trans(coordinates))


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

    def __init__(self, bdd):
        """
        Constructor for a PrettyPrintBDD class.
        :param bdd: The BDD to print.
        """
        self.bdd = bdd
        self.graph = nx.MultiDiGraph()  # multiedges between nodes
        self.labels = dict()  # dictionary to store labels of nodes in

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
                    edge_data['connectionstyle'] = 'arc3,rad=-0.3'
                else:
                    edge_data['connectionstyle'] = 'arc3,rad=0.3'
            nx.draw_networkx_edges(self.graph, pos, [edge], **edge_data)

    def _draw_labels(self, pos):
        """
        Draw the labels of the BDD graph.
        :param pos: The positions of the nodes.
        """
        nx.draw_networkx_labels(self.graph, pos, self.labels)
