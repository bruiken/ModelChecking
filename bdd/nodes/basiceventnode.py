from bdd.nodes.basenode import Node


class BasicEventNode(Node):
    """
    Node for a BDD which is not a leaf node.
    """

    def __init__(self, node_true, node_false, basic_event):
        """
        BasicEventNode constructor, takes a node for the "true"
        path, a node for the "false" path and a name.
        """
        super().__init__()
        self.node_true = node_true
        self.node_false = node_false
        self.basic_event = basic_event

    def calculate_probability(self):
        """
        Calculates the probability of a BasicEventNode.
        This is done by calculating the probabilities of the children
        and then multiplying them by the probability of the basis event
        or (1 - prob_basic_event) (depending on the true- or false-path
        respectively).
        """
        false_prob = self.node_false.calculate_probability()
        true_prob = self.node_true.calculate_probability()
        return false_prob * (1 - self.basic_event.get_probability()) + \
            true_prob * self.basic_event.get_probability()

    def has_children(self):
        """
        Returns True as a basic event does have child nodes.
        """
        return True

    def get_basic_event(self):
        """
        Gets the BasicEvent class that represents the basic event in the
        node.
        """
        return self.basic_event

    def get_true_node(self):
        """
        Returns the node that is reached when taking the "True" path.
        """
        return self.node_true

    def get_false_node(self):
        """
        Returns the node that is reached when taking the "False" path.
        """
        return self.node_false

    def get_name(self):
        """
        Returns the name of the node.
        """
        return self.basic_event.get_name()

    def get_leaf_nodes(self):
        """
        Get the leaf nodes of a BasicEventNode. We first take the leaf
        nodes from the "true" node. If there is only one element in it,
        we have to look into the other node as well, as there might be
        a different leaf node that can be reached in there.
        :return: A set of leaf nodes reachable from this node.
        """
        leaves = self.node_true.get_leaf_nodes()
        if len(leaves) == 1:
            leaves = leaves.union(self.node_false.get_leaf_nodes())
        return leaves
