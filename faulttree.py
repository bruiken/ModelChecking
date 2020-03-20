from itertools import islice
from fractions import Fraction
import collections
import re


class GalileoParseException(Exception):
    """
    GalileoParseException is an exception used when the parsing of a
    Galileo-formatted file failed.
    """

    pass


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


class BasicEvent(Gate):
    """
    A BasicEvent is a leaf node in a fault tree. It is also a Gate.
    """

    def __init__(self, name, initial_state=False, initial_probability=0.):
        """
        Constructor for a BasicEvent. This calls the constructor for the
        super with an empty set of empty child gates.
        :param name: Name of the BasicEvent.
        :param initial_state: Initial state of the BasicEvent.
        :param initial_probability: Initial probability of the BasicEvent.
               When supplying a fraction use a string ('1/7') or an
               instance of the class Fraction.
        """
        super().__init__('BASIC', name, [])
        self.state = initial_state
        self.probability = None
        self.set_probability(initial_probability)

    def operation(self):
        """
        The operation for a BasicEvent ignores the input and returns the
        state of it.
        """
        return lambda _: self.state

    def set_state(self, state):
        """
        Set the state of a BasicEvent, should be a boolean value.
        :param state: The new state, either True or False.
        """
        self.state = state

    def set_probability(self, prob):
        """
        Set the probability of a BasicEvent.
        When supplying a fraction use a string ('1/7') or an instance of
        the class Fraction.
        :param prob: The new probability.
        """
        self.probability = Fraction(str(prob))

    def get_probability(self):
        """
        Returns the probability of the basic event.
        Note that this is an instance of Fraction.
        """
        return self.probability

    def get_state(self):
        """"
        Returns the current state of the basic event.
        """
        return self.state


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
        super().__init__('AND', name, input_gates, './gates/andgate.png')

    def operation(self):
        """
        The operation for an AndGate is the all function, since all values
        should be True.
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
        super().__init__('OR', name, input_gates, 'gates/orgate.png')

    def operation(self):
        """
        The operation for an OrGate is the any function, since any of the
        values may be True for the whole gate to be true.
        """
        return any


class VotGate(Gate):
    """
    A VotGate is a gate that fails when at least k/n of its children fail.
    """

    def __init__(self, name, fail_treshold, input_gates):
        """
        The constructor for a VotGate.
        :param name: The name of the VotGate.
        :param input_gates: The child Gates.
        """
        super().__init__('VOT', name, input_gates, './gates/votgate.png')
        self.fail_treshold = fail_treshold

    def operation(self):
        """
        The operation for an VotGate is counting how many children are
        True, and if this number exceeds (or equals) the treshold, True is
        returned.
        https://stackoverflow.com/a/40351371
        """
        return lambda x: next(
            islice((y for y in x if y), self.fail_treshold - 1, None),
            False
        )

    def get_name(self):
        return '{} ({}/{})'.format(
            self.name,
            self.fail_treshold,
            len(self.input_gates)
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
        super().__init__('NOT', name, [input_gate], './gates/notgate.png')

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
        super().__init__('XOR', name, input_gates, './gates/xorgate.png')

    @staticmethod
    def xor_check(results):
        """
        Helper function to determine the result of the XOR-gate. Returns
        True iff exactly input of the gates is True.
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
        The operation for the XorGate. Uses the helper function xor_check.
        :return:
        """
        return self.xor_check


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


class _InputReader:
    """
    Base class for an input reader.
    """

    def __init__(self, file):
        """
        Cosntructor for an InputReader.
        Takes the path to the file as an argument.
        """
        self.file = file
        self.contents = self.get_contents()

    def get_contents(self):
        """
        Get the contents of the file given to the constructor.
        """
        with open(self.file, 'r') as f:
            return f.read()

    def create_faulttree(self):
        """
        The base implementation for create_faulttree, this does nothing.
        Must be overridden.
        """
        pass


class GalileoReader(_InputReader):
    """
    The GalileoReader can create a faulttree from the Galileo format.
    """

    def __init__(self, file):
        """
        Costructor for a GalileoReader, takes as an argument the file to
        read from.
        """
        super().__init__(file)
        self.gates = {}
        self.toplevel = None
        self.created_gates = {}
        self.basic_events = {}

    def create_faulttree(self):
        """
        Creates te faulttree. This is done by first parsing the file, and
        then using the create_gates function to create the actual
        faulttree from the parsed system.

        :raises: GalileoParseException: If the tree could not be created.
        """
        self.parse_file()
        if not self.toplevel:
            raise GalileoParseException('Toplevel is not defined')
        else:
            system = self.create_gates(self.toplevel)
            return FaultTree(self.toplevel, self.basic_events, system)

    def create_gates(self, gate_name):
        """
        Create gates creates the faulttree for the given gate name.
        We do this by first checking if we already created the gate, if
        this is not the case then we create it using the create_gate
        function.
        :param gate_name: The gate name to create the gate for.
        :return: The created gate.
        :raises: GalileoParseException: If the tree could not be created.
        """
        if gate_name in self.created_gates:
            return self.created_gates[gate_name]
        elif gate_name in self.gates:
            return self.create_gate(gate_name)
        else:
            raise GalileoParseException(
                'Missing constructor for gate "{}"'.format(gate_name)
            )

    def create_gate(self, name):
        """
        The create_gate function creates a new entry to the cached gates.
        If the gate has input gates, recursively call the create_gates
        function.
        :param name: The name of the gate to be created.
        :return: The created gate.
        """
        construct, options = self.gates[name]
        if 'input_gates' in options:
            options['input_gates'] = list(map(
                lambda x: self.create_gates(x), options['input_gates']
            ))
        gate = construct(name, **options)
        self.created_gates[name] = gate
        if isinstance(gate, BasicEvent):
            self.basic_events[name] = gate
        return gate

    def parse_file(self):
        """
        Parses the given file to read all the gates.
        :raises: GalileoParseException: If the file could not be parsed.
        """
        for line in self.contents.split('\n'):
            self.parse_line(line)

    def parse_line(self, line):
        """
        Parses one line from a file in Galileo format.
        :param line: The line to parse.
        :raises: GalileoParseException: If the file could not be parsed.
        """
        args = line.rstrip(';').split()
        if args[0] == 'toplevel':
            self.parse_toplevel(args)
        elif len(args) > 1 and GalileoReader.is_gate(args[1]):
            self.parse_gate(args)
        else:
            self.parse_basic_event(args)

    def parse_toplevel(self, args):
        """
        Parses a line that defines the toplevel.
        :param args: A list of arguments that describes the line.
        :raises: GalileoParseException: If the file could not be parsed.
        """
        if self.toplevel:
            raise GalileoParseException('Toplevel is defined twice')
        else:
            self.toplevel = GalileoReader.read_name(args[1])

    @staticmethod
    def is_gate(gate):
        """
        Checks whether the given name is a gate.
        :param gate: The name to check.
        :return: True if the given name is a gate.
        """
        return gate in ['and', 'or'] or re.match(r'^\d+of\d+$', gate)

    def parse_gate(self, args):
        """
        Parses a line that describes a gate.
        This also creates an entry in the self.gates dictionary.
        :param args: The arguments that describe the gate.
        :raises: GalileoParseException: If the name is not in a correct
                 format.
        """
        name = GalileoReader.read_name(args[0])
        if name not in self.gates:
            self.gates[name] = GalileoReader.get_gate(args[1])
            for gate in args[2:]:
                gate_name = GalileoReader.read_name(gate)
                self.gates[name][1]['input_gates'].append(gate_name)

    @staticmethod
    def get_gate(gate):
        """
        Create a construct for a gate.
        We use this later when actually creating the gates. We cannot
        actually create the gates already as we first need to parse the
        entire file.
        :param gate: The gate to create a construct for.
        :return: A tuple containing the class for the Gate and the args
                 for it.
        :raises: GalileoParseException: If not suitable Gate could be
                                        found.
        """
        if gate == 'and':
            return AndGate, {'input_gates': []}
        elif gate == 'or':
            return OrGate, {'input_gates': []}
        else:
            match = re.match(r'^(\d+)of\d+$', gate)
            if match:
                return VotGate, {'fail_treshold': int(match[1]),
                                 'input_gates': []}
        raise GalileoParseException(
            'No suitable gate found for "{}"'.format(gate)
        )

    def parse_basic_event(self, args):
        """
        Parses a line that describes a basic event.
        :param args: The arguments that describe the basic event.
        :raises: GalileoParseException: If the name is not in a correct
                 format.
        """
        name = GalileoReader.read_name(args[0])
        attrs = GalileoReader.parse_basic_event_args(args[1:])
        options = dict()
        if 'prob' in attrs:
            options['initial_probability'] = attrs['prob']
        self.gates[name] = BasicEvent, options

    @staticmethod
    def parse_basic_event_args(args):
        """
        Parses the basic event args. We use this to parse the extra
        options in the basic event in the form of ``key=val''.
        :param args: The arguments given to the basic event.
        :return: A dicionary containing the key-value pairs.
        """
        result = dict()
        for arg in args:
            key, val = arg.split('=')
            result[key] = val
        return result

    @staticmethod
    def read_name(word):
        """
        Read a name in the Galileo file.
        This can be either something in the form "foo", for which we only
        want the *foo* part. Or just *foo*.
        :param word: The name we want to parse.
        :return: The name in the word.
        :raises: GalileoParseException: If the name is not in a correct
                 format.
        """
        if word.startswith('"'):
            if word.endswith('"') and len(word) > 2:
                return word[1:-1]
            raise GalileoParseException('Invalid name "{}"'.format(word))
        return word


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
