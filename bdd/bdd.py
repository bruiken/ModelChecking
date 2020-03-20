class BDD:
    """
    The BDD class is used to represent a BDD.
    It has a system which is an instance of a Node.
    """

    def __init__(self, system):
        """
        The constructor for a BDD takes as an argument an instance of
        Node.
        :param system: The Node describing the BDD.
        """
        self.system = system

    def calculate_probability(self):
        """
        Calculates the probability of the entire BDD using the
        probabilities stored in the basic events.
        """
        return self.system.calculate_probability()

    def get_system(self):
        """
        Get the entire system of the BDD.
        """
        return self.system
