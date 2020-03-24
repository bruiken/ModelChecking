from bdd.nodes import LeafNode, BasicEventNode
from bdd.bdd import BDD


class BDDMinimiser:
    """
    A BDDMinimiser can minimise a given BDD.
    This means that unnecessary nodes and edges from an existing BDD will
    be removed. This is done using the get_leaf_nodes() function defined
    by Node instances.
    """

    def __init__(self, bdd):
        """
        Initialiser for a BDDMinimiser class. Takes as an argument the BDD
        to minimise.
        :param bdd: The BDD to minimise.
        """
        self.bdd = bdd

    def minimise(self):
        """
        The minimise function minimises the BDD by removing unnecessary
        nodes and edges.
        :return: A new BDD consisting of new Nodes that is the minimised
                 version of the old BDD.
        """
        return BDD(self._minimise(self.bdd.get_system()))

    def _minimise(self, node):
        """
        This function actually does the minimising.
        Finds out the leaf nodes of the given node, if this is only one
        leaf node, then we can return just a new LeafNode. If there are
        multiple leaf nodes, we have to create a new BasicEventNode with
        the "true" and "false" nodes which are also minimised recursively.
        :param node: The current node to minimise.
        :return: A new instance of a Node.
        """
        leaves = node.get_leaf_nodes()
        if len(leaves) == 1:
            return LeafNode(leaves.pop())
        else:
            return BasicEventNode(
                self._minimise(node.get_true_node()),
                self._minimise(node.get_false_node()),
                node.get_basic_event())
