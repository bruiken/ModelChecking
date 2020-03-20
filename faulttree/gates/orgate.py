from faulttree.gates.basegate import Gate


class OrGate(Gate):
    """
    An OrGate is the representation for the logical OR-gate.
    """

    def __init__(self, name, input_gates):
        """
        The constructor for an OrGate.
        :param name: The name of the OrGate.
        :param input_gates: The child Gates.
        """
        super().__init__('OR', name, input_gates, './resources/orgate.png')

    def operation(self):
        """
        The operation for an OrGate is the any function, since any of the
        values may be True for the whole gate to be true.
        """
        return any
