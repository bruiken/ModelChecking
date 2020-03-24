import collections
from faulttree.gates import BasicEvent


class FaultTree:
    """
    The FaultTree class defines a complete FaultTree.
    It has a Gate as its system, a number of basic events and a name.
    """

    def __init__(self, name, system):
        """
        The constructor for a FaultTree.
        :param name: The name of the FaultTree.
        :param system: The Gate of the system.
        """
        self.name = name,
        self.system = system
        self.gates = {
            x.get_unique_index(): x for x in self._construct_gates()
        }
        self.basic_events = self._get_basic_events()

    def _get_basic_events(self):
        result = {}
        for k, v in self.gates.items():
            if isinstance(v, BasicEvent):
                result[k] = v
        return result

    def set_state(self, index, state):
        """
        Sets the state of some basic event to the given value.
        :param index: The index of the basic event.
        :param state: The new state for the given event.
        """
        if index in self.basic_events:
            self.basic_events[index].set_state(state)

    def set_states(self, states):
        """
        Sets the states for many basic events at once.
        The input should be a dictionary keyed on the indices of the basic
        events, values are boolean.
        """
        for index, state in states.items():
            self.set_state(index, state)

    def set_probability(self, index, prob):
        """
        Sets the probability of some basic event to the given value. When
        supplying a fraction use a string ('1/7') or an instance of the
        class Fraction.
        :param index: The index of the basic event.
        :param prob: The new probability for the given event.
        """
        if index in self.basic_events:
            self.basic_events[index].set_probability(prob)

    def set_probabilities(self, probabilities):
        """
        Sets multiple probabilities of basic events at once.
        Uses the set_probability function multiple times.
        The input should be a dictionary keyed on the names of the basic
        events and valued with their probabilities. When supplying a
        fraction use a string ('1/7') or an instance of the class
        Fraction.
        """
        for index, prob in probabilities.items():
            self.set_probability(index, prob)

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

    def get_basic_event(self, index):
        """
        Returns the basic event with the given index or None if it does
        not exist.
        """
        if index in self.basic_events:
            return self.basic_events[index]
        return None

    def _construct_gates(self):
        """
        Constructs the set of all Gates in the system and returns it.
        """
        def gates(x):
            return [x.input_gates] + \
                   [gates(y) for y in x.input_gates if x.input_gates]

        return list(flatten(gates(self.system))) + [self.system]

    def get_gate(self, index):
        """
        Returns the first gate in the system matching the given index or
        None if there is no matching gate.
        """
        if index in self.gates:
            return self.gates[index]
        return None

    def get_basic_events(self):
        """
        Returns the dictionary of basic events.
        """
        return self.basic_events

    def get_system(self):
        """
        Returns the system of the Fault Tree.
        """
        return self.system

    def max_depth(self):
        """
        Gets the maximum depth of the system.
        :return: The height of the system.
        """
        return self._max_depth(self.system, 0)

    def _max_depth(self, gate, depth):
        """
        Calculates the max depth of the given gate recursively).
        :param gate: The current gate.
        :param depth: The current depth.
        :return: the maximum depth from the given gate.
        """
        if isinstance(gate, BasicEvent):
            return depth
        return max(
            self._max_depth(x, depth+1) for x in gate.get_input_gates()
        )


def flatten(l):
    """
    Flattens a list of elements. This list can contain any depth of lists,
    and it will be converted to a 1 dimensional list.
    """
    for el in l:
        if isinstance(el, collections.Iterable) and \
                not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el
