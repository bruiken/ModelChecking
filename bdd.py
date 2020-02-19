class Node:
    """
    The node class is the abstract class used by BDD nodes.
    """

    def calculate_probability(self):
        """
        Calculates the probability fo the given node.
        """
        return 0


class BasicEventNode(Node):
    """
    Node for a BDD which is not a leaf node.
    """

    def __init__(self, node_true, node_false, basic_event):
        """
        BasicEventNode constructor, takes a node for the "true"
        path, a node for the "false" path and a name.
        """
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

    def __str__(self):
        return '{}: TRUE -> ({}) FALSE -> ({})'.format(
            self.basic_event.get_name(),
            str(self.node_true),
            str(self.node_false)
        )


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
        self.value = value

    def calculate_probability(self):
        """
        Calculates the probability of a LeafNode.
        This is just the integer representation of the value, True
        is 1, False is 0.
        """
        return int(self.value)

    def __str__(self):
        return str(self.value)


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
