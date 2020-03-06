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
        self.idx = Node.index
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
        return self.idx

    def get_leaf_nodes(self):
        """
        Function that gets the number of leaf nodes reachable from the
        current node.
        Should return a set of leaf nodes.
        """
        pass


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


class LeafNode(Node):
    """
    LeafNodes are for leaf nodes in BDDs. They can either be True
    or False.
    """

    def __init__(self, value):
        """
        Constructor for a LeafNode. Takes a value which can be
        True or False.
        """
        super().__init__()
        self.value = value

    def calculate_probability(self):
        """
        Calculates the probability of a LeafNode.
        This is just the integer representation of the value, True
        is 1, False is 0.
        """
        return int(self.value)

    def get_name(self):
        """
        Get the name of the LeafNode, which is either the string "True" or
        "False".
        """
        return str(int(self.value))

    def get_value(self):
        """
        Get the value of the LeafNode. Which is either True or False.
        """
        return self.value

    def get_unique_name(self):
        """
        Get the unique name of the leaf node, which is its value.
        """
        return self.value

    def get_leaf_nodes(self):
        """
        Get the leaf nodes of the leaf node, this is just a singleton set
        with its value.
        :return:
        """
        return {self.value}


class BDDConstructor:
    """
    The BDDConstructor can translate a Fault Tree into a BDD.
    """

    def __init__(self, fault_tree):
        """
        Constructor for the BDDConstructor. Takes as an argument
        the fault tree to be converted.
        """
        self.fault_tree = fault_tree

    def construct_bdd(self, ordering, minimise=True):
        """
        Constructs a BDD with the given ordering.
        :param ordering: The ordering to use for the construction.
        :param minimise: Whether or not to minimise the BDD after
                         construction.
        :return: the created system.
        """
        var_ordering = ordering.order_variables(self.fault_tree)
        bdd = BDD(self._construct_bdd(
            var_ordering,
            self.fault_tree.get_false_state()
        ))
        if minimise:
            return BDDMinimiser(bdd).minimise()
        else:
            return bdd

    def _construct_bdd(self, variable_ordering, state):
        """
        The construct_bdd function takes the remaining variable
        ordering and the current state to create a new layer
        of the final BDD.
        This function works depth first.
        """
        self.fault_tree.set_states(state)
        fault_tree_holds = self.fault_tree.apply()
        if fault_tree_holds or not variable_ordering:
            return LeafNode(fault_tree_holds)
        else:
            return self._construct_node(
                variable_ordering[0],
                variable_ordering[1:],
                state
            )

    def _construct_node(self, variable, variable_ordering, state):
        """
        Construct_node is a helper function to create the entire BDD.
        It constructs a non-leaf-node.
        """
        state[variable] = True
        true_node = self._construct_bdd(variable_ordering, state)
        state[variable] = False
        false_node = self._construct_bdd(variable_ordering, state)
        return BasicEventNode(
            true_node,
            false_node,
            self.fault_tree.get_basic_event(variable)
        )


class BDD:
    """
    The BDD class is used to represent a BDD.
    It has a system which is an instance of a Node.
    """

    def __init__(self, system):
        """
        The constructor for a BDD takes as an argument an instance of
        Node.
        :param system: The Node describing the BDD.
        """
        self.system = system

    def calculate_probability(self):
        """
        Calculates the probability of the entire BDD using the
        probabilities stored in the basic events.
        """
        return self.system.calculate_probability()

    def get_system(self):
        """
        Get the entire system of the BDD.
        """
        return self.system


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
