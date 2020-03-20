class Gate:
    """
    Abstract class for a Gate.
    Implementations should implement the "operation" function.
    """

    index = 0   # unique index

    def __init__(self, gate_type, name, input_gates, image_path=None):
        """
        Constructor for a Gate.
        :param gate_type: type of the gate.
        :param name: name for the gate.
        :param input_gates: a list of Gates.
        :param image_path: the path to he image representing the gate.
        """
        self.name = name
        self.gate_type = gate_type
        self.input_gates = input_gates
        self.image_path = image_path
        self.idx = Gate.index
        Gate.index += 1

    def apply(self, print_trace):
        """
        The base implementation for apply.
        Gets the operator of the current gate and applies it on the map of
        the apply function on the child gates.
        :return: Whether or not the Gate is satisfied.
        """
        if print_trace:
            print('apply {}'.format(self.name))
        op = self.operation()
        result = op(map(lambda x: x.apply(print_trace), self.input_gates))
        return result

    def operation(self):
        """
        The base implementation for the operation function.
        This function should take a list of Boolean values and produce a
        Boolean value as result.
        Must be overridden.
        """
        return lambda _: True

    def get_name(self):
        """
        Returns the name of the gate.
        """
        return self.name

    def get_image_path(self):
        """
        Returns the path to the image representing the gate.
        """
        return self.image_path

    def get_input_gates(self):
        """
        Returns the input gates of the Gate.
        """
        return self.input_gates

    def get_unique_index(self):
        """
        Get the unique index of the gate.
        """
        return self.idx
