from bdd.nodes.basenode import Node


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
