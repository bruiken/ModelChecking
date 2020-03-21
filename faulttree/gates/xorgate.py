from faulttree.gates.basegate import Gate


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
        super().__init__('XOR', name, input_gates, './resources/xorgate.png')

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
