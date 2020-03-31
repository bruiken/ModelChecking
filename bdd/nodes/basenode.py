class Node:
    """
    The node class is the abstract class used by BDD nodes.
    """

    index = 0  # index to uniquely name each node

    def __init__(self):
        """
        Initialiser for a Node, this just sets the unique index and then
        increases the counter for the unique indices.
        """
        self._idx = Node.index
        Node.index += 1

    def calculate_probability(self):
        """
        Calculates the probability fo the given node.
        """
        return 0

    def has_children(self):
        """
        Returns whether or not the node has child nodes.
        """
        return False

    def get_name(self):
        """
        Get the name of the node.
        """
        return None

    def get_unique_name(self):
        """
        Get the unique name for this node, by default this corresponds to
        the unique index given to it.
        """
        return self._idx

    def get_leaf_nodes(self):
        """
        Function that gets the number of leaf nodes reachable from the
        current node.
        Should return a set of leaf nodes.
        """
        pass
