from variableorderings.baseordering import Ordering


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
