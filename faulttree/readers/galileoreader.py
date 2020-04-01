from faulttree.readers.basereader import InputReader
from exceptions import GalileoParseException
import re
from faulttree.gates import AndGate, OrGate, BasicEvent, VotGate
from faulttree import FaultTree


class GalileoReader(InputReader):
    """
    The GalileoReader can create a faulttree from the Galileo format.
    """

    def __init__(self, file):
        """
        Costructor for a GalileoReader, takes as an argument the file to
        read from.
        """
        super().__init__(file)
        self._gates = {}
        self._toplevel = None
        self._created_gates = {}

    def create_faulttree(self):
        """
        Creates te faulttree. This is done by first parsing the file, and
        then using the create_gates function to create the actual
        faulttree from the parsed system.

        :raises: GalileoParseException: If the tree could not be created.
        """
        self._parse_file()
        if not self._toplevel:
            raise GalileoParseException('Toplevel is not defined')
        else:
            system = self._create_gates(self._toplevel)
            return FaultTree(self._toplevel, system)

    def _create_gates(self, gate_name):
        """
        Create gates creates the faulttree for the given gate name.
        We do this by first checking if we already created the gate, if
        this is not the case then we create it using the create_gate
        function.
        :param gate_name: The gate name to create the gate for.
        :return: The created gate.
        :raises: GalileoParseException: If the tree could not be created.
        """
        if gate_name in self._created_gates:
            return self._created_gates[gate_name]
        elif gate_name in self._gates:
            return self._create_gate(gate_name)
        else:
            raise GalileoParseException(
                'Missing constructor for gate "{}"'.format(gate_name)
            )

    def _create_gate(self, name):
        """
        The create_gate function creates a new entry to the cached gates.
        If the gate has input gates, recursively call the create_gates
        function.
        :param name: The name of the gate to be created.
        :return: The created gate.
        """
        construct, options = self._gates[name]
        if 'input_gates' in options:
            options['input_gates'] = list(map(
                lambda x: self._create_gates(x), options['input_gates']
            ))
        gate = construct(name, **options)
        self._created_gates[name] = gate
        return gate

    def _parse_file(self):
        """
        Parses the given file to read all the gates.
        :raises: GalileoParseException: If the file could not be parsed.
        """
        for line in self._contents.split('\n'):
            self._parse_line(line)

    def _parse_line(self, line):
        """
        Parses one line from a file in Galileo format.
        :param line: The line to parse.
        :raises: GalileoParseException: If the file could not be parsed.
        """
        args = line.rstrip(';').split()
        if len(args) == 0:
            return
        elif args[0] == 'toplevel':
            self._parse_toplevel(args)
        elif len(args) > 1 and GalileoReader._is_gate(args[1]):
            self._parse_gate(args)
        else:
            self._parse_basic_event(args)

    def _parse_toplevel(self, args):
        """
        Parses a line that defines the toplevel.
        :param args: A list of arguments that describes the line.
        :raises: GalileoParseException: If the file could not be parsed.
        """
        if self._toplevel:
            raise GalileoParseException('Toplevel is defined twice')
        else:
            self._toplevel = GalileoReader._read_name(args[1])

    @staticmethod
    def _is_gate(gate):
        """
        Checks whether the given name is a gate.
        :param gate: The name to check.
        :return: True if the given name is a gate.
        """
        return gate in ['and', 'or'] or re.match(r'^\d+of\d+$', gate)

    def _parse_gate(self, args):
        """
        Parses a line that describes a gate.
        This also creates an entry in the self.gates dictionary.
        :param args: The arguments that describe the gate.
        :raises: GalileoParseException: If the name is not in a correct
                 format.
        """
        name = GalileoReader._read_name(args[0])
        if name not in self._gates:
            self._gates[name] = GalileoReader._get_gate(args[1])
            for gate in args[2:]:
                gate_name = GalileoReader._read_name(gate)
                self._gates[name][1]['input_gates'].append(gate_name)

    @staticmethod
    def _get_gate(gate):
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

    def _parse_basic_event(self, args):
        """
        Parses a line that describes a basic event.
        :param args: The arguments that describe the basic event.
        :raises: GalileoParseException: If the name is not in a correct
                 format.
        """
        name = GalileoReader._read_name(args[0])
        attrs = GalileoReader._parse_basic_event_args(args[1:])
        options = dict()
        if 'prob' in attrs:
            options['initial_probability'] = attrs['prob']
        self._gates[name] = BasicEvent, options

    @staticmethod
    def _parse_basic_event_args(args):
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
    def _read_name(word):
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
