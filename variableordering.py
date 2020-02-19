from random import shuffle


class Ordering:
    """
    Abstract class for variable ordering.
    Implementations should implement the "order_variables" function.
    """

    def __init__(self, ordering_type):
        """
        Constructor for a variable ordering.
        :param ordering_type: type of the ordering (algorithm used)
        """
        self.ordering_type = ordering_type

    def order_variables(self, fault_tree):
        """
        Returns a variable ordering that just takes the order of
        variables of in the Fault Tree.
        """
        return list(fault_tree.get_basic_events().keys())


class RandomOrdering(Ordering):
    """
    RandomOrdering is the randomly chosen variable ordering.
    """

    def __init__(self):
        """
        Constructor for a RandomOrdering.
        """
        super().__init__('Random')

    def order_variables(self, fault_tree):
        """
        Order the variables randomly and return the ordering.
        """
        ordering = list(fault_tree.get_basic_events().keys())
        shuffle(ordering)
        return ordering


class ManualOrdering(Ordering):
    """
    ManualOrdering is a ordering which can be set manually.
    """

    def __init__(self, ordering):
        """
        Constructor for a ManualOrdering.
        :param ordering: The manually chosen ordering.
        """
        super().__init__('Manual')
        self.ordering = ordering

    def order_variables(self, fault_tree):
        """
        Returns the manual ordering with which the class was created.
        """
        return self.ordering
