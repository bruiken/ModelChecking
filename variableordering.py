from random import shuffle


class Ordering:
    """
    Abstract class for variable ordering.
    Implementations should implement the "order_variables" function.
    """

    def __init__(self, ordering_type, fault_tree):
        """
        Constructor for a variable ordering.
        :param ordering_type: type of the ordering (algorithm used)
        :param fault_tree: the Fault Tree for which the variables
                            are ordered
        """
        self.ordering_type = ordering_type
        self.fault_tree = fault_tree

    def order_variables(self):
        """
        Returns a variable ordering that just takes the order of
        variables of in the Fault Tree.
        """
        return list(self.fault_tree.get_basic_events().keys())


class RandomOrdering(Ordering):
    """
    RandomOrdering is the randomly chosen variable ordering.
    """

    def __init__(self, fault_tree):
        """
        Constructor for a RandomOrdering.
        :param fault_tree: the Fault Tree for which the variables
                            are ordered
        """
        super().__init__('Random', fault_tree)

    def order_variables(self):
        """
        Order the variables randomly and return the ordering.
        """
        ordering = list(self.fault_tree.get_basic_events().keys())
        shuffle(ordering)
        return ordering
