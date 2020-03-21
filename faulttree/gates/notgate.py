from faulttree.gates.basegate import Gate


class NotGate(Gate):
    """
    A NotGate is a representation for a logical NOT-gate.
    It takes 1 and at most 1 input gate.
    """

    def __init__(self, name, input_gate):
        """
        The constructor for a NotGate.
        :param name: The name of the NotGate.
        :param input_gate: The child Gate of the NotGate.
        """
        super().__init__('NOT', name, [input_gate], './resources/notgate.png')

    def operation(self):
        """
        The operation for a NotGate inverts the result of its child.
        Note that there is a list constructor, this is to be able to use
        the subscript (the argument of the function will be a generator).
        :return:
        """
        return lambda x: not list(x)[0]
