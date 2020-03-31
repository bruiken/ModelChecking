import matplotlib.pyplot as plt


class PrettyPrint:
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

    def print_to_file(self, filename, dpi=None, size=(10, 10)):
        """
        Prints the current figure to a file.
        :param filename: The filename.
        :param dpi: The DPI of the drawing.
        :param size: Tuple with the size of the figure in inches.
        """
        plt.clf()
        self._pretty_print()
        plt.gcf().set_size_inches(*size)
        plt.savefig(filename, dpi=dpi)

    def print_to_window(self, size=(10, 10)):
        """
        Prints the current figure to a window.
        :param size: Tuple with the size of the figure in inches.
        """
        plt.clf()
        self._pretty_print()
        plt.gcf().set_size_inches(*size)
        plt.show()
