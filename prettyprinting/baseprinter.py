import matplotlib.pyplot as plt


class _PrettyPrint:
    """
    Base class for pretty printers.
    Pretty printers must override the _pretty_print function.
    """

    def _pretty_print(self):
        """
        The pretty print function must be overriden and sets up the pretty
        printing. The pretty printing should be done in matplotlib such
        that savefig and show can be called on it.
        """
        pass

    def print_to_file(self, filename, dpi=None):
        """
        Prints the current figure to a file.
        :param filename: The filename.
        :param dpi: The DPI of the drawing.
        """
        self._pretty_print()
        plt.savefig(filename, dpi=dpi)

    def print_to_window(self):
        """
        Prints the current figure to a window.
        """
        self._pretty_print()
        plt.show()
