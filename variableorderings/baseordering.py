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

    def get_ordering_type(self):
        """
        Returns the name of the ordering.
        """
        return self.ordering_type
