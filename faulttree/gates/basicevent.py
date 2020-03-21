from faulttree.gates.basegate import Gate
from fractions import Fraction


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
