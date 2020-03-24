from variableorderings.baseordering import Ordering
from faulttree.gates import BasicEvent


class BFSOrdering(Ordering):
    """
    The BFS Ordering is an ordering based on breath first search.
    The ordering is based on how deep a certain BasicEvent lies in the
    system. It can either do top to bottom or bottom to top based on a
    flag given in the initialiser.
    """

    def __init__(self, bottom_to_top=True):
        """
        Initialiser for a BFSOrdering.
        :param bottom_to_top: Whether to order from bottom to top
                              (the default) or top to bottom.
        """
        super().__init__('Topological ordering')
        self.bottom_to_top = bottom_to_top
        self.depths = {}

    def order_variables(self, fault_tree):
        """
        Order the variables based on their depth.
        :param fault_tree: The fault tree to order the BasicEvents of.
        :return: The ordering of the variables.
        """
        self.parse_depth(fault_tree.get_system(), 0, fault_tree)
        top_to_bot = sorted(self.depths.keys(),  # sort dictionary values
                            key=lambda x: self.depths[x])
        if self.bottom_to_top:
            return reversed(top_to_bot)
        else:
            return top_to_bot

    def parse_depth(self, gate, depth, fault_tree):
        """
        Calculates the depths of the basic events in a recursive way.
        The depths are saved in a dictionary saved in the class (depths).
        :param gate: The gate currently parsing.
        :param depth: The current depth.
        :param fault_tree: The fault tree to parse.
        """
        name = gate.get_name()
        if isinstance(gate, BasicEvent):
            if name not in self.depths or depth < self.depths[name]:
                self.depths[fault_tree.get_basic_event_key(gate)] = depth
        else:
            for child in gate.get_input_gates():
                self.parse_depth(child, depth+1, fault_tree)
