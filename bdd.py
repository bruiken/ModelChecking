class BasicEventNode:
    """
    Node for a BDD which is not a leaf node.
    """

    def __init__(self, node_true, node_false, name):
        """
        BasicEventNode constructor, takes a node for the "true"
        path, a node for the "false" path and a name.
        """
        self.node_true = node_true
        self.node_false = node_false
        self.name = name

    def __str__(self):
        return '{}: TRUE -> ({}) FALSE -> ({})'.format(
            self.name,
            str(self.node_true),
            str(self.node_false)
        )


class LeafNode:
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

    def construct_bdd(self, variable_ordering, state):
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
            return self.construct_node(
                variable_ordering[0],
                variable_ordering[1:],
                state
            )

    def construct_node(self, variable, variable_ordering, state):
        """
        Construct_node is a helper function to create the entire BDD.
        It constructs a non-leaf-node.
        """
        state[variable] = True
        true_node = self.construct_bdd(variable_ordering, state)
        state[variable] = False
        false_node = self.construct_bdd(variable_ordering, state)
        return BasicEventNode(true_node, false_node, variable)
