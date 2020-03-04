class Node:
    """
    The node class is the abstract class used by BDD nodes.
    """

    index = 0  # index to uniquely name each node

    def __init__(self):
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
        return str(int(self.value))

    def get_value(self):
        return self.value

    def get_unique_name(self):
        return self.value


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

    def construct_bdd(self, ordering):
        """
        Constructs a BDD with the given ordering.
        :return the created system.
        """
        var_ordering = ordering.order_variables(self.fault_tree)
        return self._construct_bdd(
            var_ordering,
            self.fault_tree.get_false_state()
        )

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
