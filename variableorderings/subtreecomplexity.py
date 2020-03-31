from variableorderings.baseordering import Ordering
from faulttree.gates import BasicEvent


class SubTreeComplexity(Ordering):
    """
    The SubTreeComplexity ordering is an ordering based on how many gates
    a certain BasicEvent influences. This is also weighted by how deep a
    gate is in the tree: if it is deeper, it has a lower weight, so the
    BasicEvent will get a lower score.
    """

    def __init__(self):
        """
        Initialiser for the SubTreeComplexity ordering.
        """
        super().__init__('Sub-Tree Complexity')
        self._complexities = {}

    def order_variables(self, fault_tree):
        """
        Orders the variable according to the SubTreeComplexity algorithm.
        :param fault_tree: Fault tree to create the ordering for.
        :return: The ordering for the variables.
        """
        self._score_events(fault_tree)
        return sorted(  # inverse sort on the values of the dictionary
            self._complexities.keys(),
            key=lambda x: -self._complexities[x]
        )

    def _score_events(self, fault_tree):
        """
        Scores the basic events by their influence in the system.
        :param fault_tree: The fault tree to score the BasicEvents of.
        """
        max_depth = fault_tree.max_depth()
        for key, event in fault_tree.get_basic_events().items():
            states = fault_tree.get_false_state()
            states[key] = True
            fault_tree.set_states(states)
            self._complexities[key] = self._score_event(
                fault_tree.get_system(),
                max_depth
            )

    def _score_event(self, gate, score):
        """
        Score an individual BasicEvent.
        The score of a BasicEvent goes up by (max_depth - current_depth)
        for a gate at depth current_depth if it enables a gate by being on
        by itself.
        :param gate: The current gate to look at.
        :param score: The current score.
        :return:
        """
        gate_score = SubTreeComplexity._get_gate_score(gate, score)
        for child in gate.get_input_gates():
            gate_score += self._score_event(child, score-1)
        return gate_score

    @staticmethod
    def _get_gate_score(gate, score):
        """
        Get the score of an individual gate.
        :param gate: The gate to get the score of.
        :param score: The score to give to the gate if it is succesfull.
        :return: Score if the gate was succesfull, else 0.
        """
        if gate.apply(False) and not isinstance(gate, BasicEvent):
            return score
        else:
            return 0
