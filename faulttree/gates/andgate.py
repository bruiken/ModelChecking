from faulttree.gates.basegate import Gate


class AndGate(Gate):
    """
    An AndGate is the representation for the logical AND-gate.
    """

    def __init__(self, name, input_gates):
        """
        The constructor for an AndGate.
        :param name: The name of the AndGate.
        :param input_gates: The child Gates.
        """
        super().__init__('AND', name, input_gates, './resources/andgate.png')

    def operation(self):
        """
        The operation for an AndGate is the all function, since all values
        should be True.
        """
        return all
