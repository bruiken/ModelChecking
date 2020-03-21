import collections


class FaultTree:
    """
    The FaultTree class defines a complete FaultTree.
    It has a Gate as its system, a number of basic events and a name.
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
        self.gates = {
            x.get_unique_index(): x for x in self._construct_gates()
        }

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
        The input should be a dictionary keyed on the names of the basic
        events, values are boolean.
        """
        for name, state in states.items():
            self.set_state(name, state)

    def set_probability(self, name, prob):
        """
        Sets the probability of some basic event to the given value. When
        supplying a fraction use a string ('1/7') or an instance of the
        class Fraction.
        :param name: The name of the basic event.
        :param prob: The new probability for the given event.
        """
        if name in self.basic_events:
            self.basic_events[name].set_probability(prob)

    def set_probabilities(self, probabilities):
        """
        Sets multiple probabilities of basic events at once.
        Uses the set_probability function multiple times.
        The input should be a dictionary keyed on the names of the basic
        events and valued with their probabilities. When supplying a
        fraction use a string ('1/7') or an instance of the class
        Fraction.
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
        Returns the basic event with the given name or None if it does not
        exist.
        """
        if name in self.basic_events:
            return self.basic_events[name]
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
