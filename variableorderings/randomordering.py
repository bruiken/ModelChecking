from variableorderings.baseordering import Ordering
from random import shuffle


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
