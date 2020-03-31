from faulttree.gates.basegate import Gate
from itertools import islice


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
        super().__init__('VOT', name, input_gates, './resources/votgate.png')
        self._fail_treshold = fail_treshold

    def operation(self):
        """
        The operation for an VotGate is counting how many children are
        True, and if this number exceeds (or equals) the treshold, True is
        returned.
        https://stackoverflow.com/a/40351371
        """
        return lambda x: next(
            islice((y for y in x if y), self._fail_treshold - 1, None),
            False
        )

    def get_name(self):
        return '{} ({}/{})'.format(
            self._name,
            self._fail_treshold,
            len(self._input_gates)
        )
