class Gate:
    """
    Abstract class for a Gate.
    Implementations should implement the "operation" function.
    """
    def __init__(self, gate_type, name, input_gates):
        """
        Constructor for a Gate
        :param gate_type: type of the gate
        :param name: name for the gate
        :param input_gates: a list of Gates
        """
        self.name = name
        self.gate_type = gate_type
        self.input_gates = input_gates

    def apply(self, print_trace=False):
        """
        The base implementation for apply.
        Gets the operator of the current gate and applies it on
        the map of the apply function on the child gates.
        :return: Whether or not the Gate is satisfied.
        """
        if print_trace:
            print('apply {}'.format(self.name))
        op = self.operation()
        result = op(map(lambda x: x.apply(), self.input_gates))
        return result

    def operation(self):
        """
        The base implementation for the operation function.
        This function should take a list of Boolean values
        and produce a Boolean value as result.
        Must be overridden.
        :return:
        """
        return lambda _: True


class BasicEvent(Gate):
    """
    A BasicEvent is a leaf node in a fault tree. It is also
    a Gate.
    """
    def __init__(self, name, initial_state=False):
        """
        Constructor for a BasicEvent. This calls the
        constructor for the super with an empty set of empty
        child gates.
        :param name: Name of the BasicEvent.
        :param initial_state: Initial state of the BasicEvent.
        """
        super().__init__('BASIC', name, [])
        self.state = initial_state

    def operation(self):
        """
        The operation for a BasicEvent ignores the input and
        returns the state of it.
        """
        return lambda _: self.state

    def set_state(self, state):
        """
        Set the state of a BasicEvent, should be a boolean
        value.
        :param state: The new state, either True or False.
        """
        self.state = state


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
        super().__init__('AND', name, input_gates)

    def operation(self):
        """
        The operation for an AndGate is the all function,
        since all values should be True.
        """
        return all


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
        super().__init__('OR', name, input_gates)

    def operation(self):
        """
        The operation for an OrGate is the any function,
        since any of the values may be True for the whole
        gate to be true.
        """
        return any


class FaultTree:
    """
    The FaultTree class defines a complete FaultTree.
    It has a Gate as its system, a number of basic events
    and a name.
    """
    def __init__(self, name, basic_events, system):
        """
        The constructor for a FaultTree.
        :param name: The name of the FaultTree.
        :param basic_events: The BasicEvents of the FaultTree.
        :param system: The Gate of the system.
        """
        self.name = name,
        self.basic_events = basic_events
        self.system = system

    def set_state(self, name, state):
        """
        Sets the state of some basic event to the given value.
        :param name: The name of the basic event.
        :param state: The new state for the given event.
        """
        if name in self.basic_events:
            self.basic_events[name].set_state(state)

    def set_states(self, states):
        """
        Sets the states for many basic events at once.
        The input should be a dictionary keyed on the names of
        the basic events, values are boolean.
        """
        for name, state in states.items():
            self.set_state(name, state)

    def apply(self):
        """
        Apply the current state on the Gate of the system.
        Returns the returning value.
        """
        return self.system.apply()

    def get_false_state(self):
        """
        Get the state where all basic events are set to False.
        """
        return {x: False for x in self.basic_events.keys()}
