class InputReader:
    """
    Base class for an input reader.
    """

    def __init__(self, file):
        """
        Cosntructor for an InputReader.
        Takes the path to the file as an argument.
        """
        self._file = file
        self._contents = self._get_contents()

    def _get_contents(self):
        """
        Get the contents of the file given to the constructor.
        """
        with open(self._file, 'r') as f:
            return f.read()

    def create_faulttree(self):
        """
        The base implementation for create_faulttree, this does nothing.
        Must be overridden.
        """
        pass
