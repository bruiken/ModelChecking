from itertools import islice
from fractions import Fraction


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

    def apply(self, print_trace):
        """
        The base implementation for apply.
        Gets the operator of the current gate and applies it on
        the map of the apply function on the child gates.
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
        This function should take a list of Boolean values
        and produce a Boolean value as result.
        Must be overridden.
        """
        return lambda _: True

    def get_name(self):
        """
        Returns the name of the gate.
        """
        return self.name


class BasicEvent(Gate):
    """
    A BasicEvent is a leaf node in a fault tree. It is also
    a Gate.
    """

    def __init__(self, name, initial_state=False, initial_probability=0.):
        """
        Constructor for a BasicEvent. This calls the
        constructor for the super with an empty set of empty
        child gates.
        :param name: Name of the BasicEvent.
        :param initial_state: Initial state of the BasicEvent.
        :param initial_probability: Initial probability of the
               BasicEvent.
        """
        super().__init__('BASIC', name, [])
        self.state = initial_state
        self.probability = None
        self.set_probability(initial_probability)

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

    def set_probability(self, prob):
        """
        Set the probability of a BasicEvent.
        :param prob: The new probability.
        """
        self.probability = Fraction(str(prob))

    def get_probability(self):
        """
        Returns the probability of the basic event.
        Note that this is an instance of Fraction.
        """
        return self.probability


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


class VotGate(Gate):
    """
    A VotGate is a gate that fails when at least k/n of its
    children fail.
    """

    def __init__(self, name, fail_treshold, input_gates):
        """
        The constructor for a VotGate.
        :param name: The name of the VotGate.
        :param input_gates: The child Gates.
        """
        super().__init__('VOT', name, input_gates)
        self.fail_treshold = fail_treshold

    def operation(self):
        """
        The operation for an VotGate is counting how many children
        are True, and if this number exceeds (or equals) the treshold,
        True is returned.
        https://stackoverflow.com/a/40351371
        """
        return lambda x: next(
            islice((y for y in x if y), self.fail_treshold - 1, None),
            False
        )


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
        super().__init__('NOT', name, [input_gate])

    def operation(self):
        """
        The operation for a NotGate inverts the result of its child.
        Note that there is a list constructor, this is to be able to use
        the subscript (the argument of the function will be a generator).
        :return:
        """
        return lambda x: not list(x)[0]


class XorGate(Gate):
    """
    XorGate is a gate that represents the logical XOR-gate.
    """

    def __init__(self, name, input_gates):
        """
        The constructor for a XorGate.
        :param name: The name of the XorGate.
        :param input_gates: The input gates.
        """
        super().__init__('XOR', name, input_gates)

    @staticmethod
    def xor_check(results):
        """
        Helper function to determine the result of the XOR-
        gate. Returns True iff exactly input of the gates is
        True.
        """
        found = False
        for result in results:
            if result:
                if not found:
                    found = True
                else:
                    return False
        return found

    def operation(self):
        """
        The operation for the XorGate. Uses the helper function
        xor_check.
        :return:
        """
        return self.xor_check


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

    def set_probability(self, name, prob):
        """
        Sets the probability of some basic event to the given
        value.
        :param name: The name of the basic event.
        :param prob: The new probability for the given event.
        """
        if name in self.basic_events:
            self.basic_events[name].set_probability(prob)

    def set_probabilities(self, probabilities):
        """
        Sets multiple probabilities of basic events at once.
        Uses the set_probability function multiple times.
        The input should be a dictionary keyed on the names
        of the basic events and valued with their
        probabilities.
        """
        for name, prob in probabilities.items():
            self.set_probability(name, prob)

    def apply(self, print_trace=False):
        """
        Apply the current state on the Gate of the system.
        Returns the returning value.
        """
        return self.system.apply(print_trace)

    def get_false_state(self):
        """
        Get the state where all basic events are set to False.
        """
        return {x: False for x in self.basic_events.keys()}

    def get_basic_event(self, name):
        """
        Returns the basic event with the given name or None if
        it does not exist.
        """
        if name in self.basic_events:
            return self.basic_events[name]
        return None
