from analysis.bdd import BDDAnalyser
from faulttree.readers import GalileoReader
from exceptions import UnsupportedFileTypeException
from time import time
from bdd import BDDConstructor, BDDMinimiser
from pathlib import Path
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


class BenchmarkResult:
    """
    The BenchmarkResult class is used to store the result of a benchmark.
    """

    def __init__(self):
        """
        Constructor for a BenchmarkResult. No arguments are given to it.
        Instead, the data is given to it using the properties.
        """
        self.ordering_time = 0
        self.construction_time = 0
        self.minimising_time = 0
        self.ordering = []
        self.bdd = None
        self.min_bdd = None
        self.bdd_nodes = 0
        self.min_bdd_nodes = 0

    def __str__(self):
        """
        The string representation for a benchmark result includes the
        number of nodes (minimised and unminimised) and the timings
        (ordering time, construction time and minimising time).
        """
        r = ''
        r += 'Timings:\n' + \
             '\tOrdering:\t\t{}s\n'.format(self.ordering_time) + \
             '\tConstruction:\t{}s\n'.format(self.construction_time) + \
             '\tMinimising:\t{}s\n'.format(self.minimising_time)
        r += 'Nodes:\n' + \
             '\tNot minimized:\t\t{}\n'.format(self.bdd_nodes) + \
             '\tMinimised:\t\t\t{}'.format(self.min_bdd_nodes)
        return r


class BDDBenchmark:
    """
    The BDDBenchmark class is a class used to benchmark the creation
    of BDDs. It can be given either a fault tree or a file. When using a
    file, it automagically detects which filetype you are supplying.
    """

    def __init__(self, file=None, fault_tree=None):
        """
        Constructor for a BDDBenchmark.
        Give either a file or a fault_tree to benchmark.
        :param file: File to benchmark.
        :param fault_tree: Fault tree to benchmark.
        :raises: UnsupportedFileTypeException: If the given file could not
                 be recognised.
        """
        if file:
            self._file = file
            self._fault_tree = self._read_file()
            self._name = Path(file).name
        else:
            self._fault_tree = fault_tree
            self._name = self._fault_tree.get_system().get_name()
        self._results = {}

    def _read_file(self):
        """
        Reads a file and determines which kind of file it is.
        :return: The created FaultTree from the file.
        :raises: UnsupportedFileTypeException: If the given file could not
                 be recognised.
        """
        filetype = self._file[self._file.rfind('.'):]
        if filetype == '.dft':
            return GalileoReader(self._file).create_faulttree()
        raise UnsupportedFileTypeException('{}'.format(filetype))

    def benchmark(self, orderings):
        """
        Benchmarks the fault tree with a number of orderings.
        We benchmark the orderings to create BDDs. What we can take from
        this is the time taken to calculate the ordering, time taken to
        construct the fault tree and time taken to minimise the BDD.
        We can also get the number of nodes of the unminimised BDD and the
        number of nodes of the minimised BDD.
        All of the results are stored in the class' "results" property.
        :param orderings: A list containing Ordering classes.
        """
        for ordering in orderings:
            self._results[ordering] = BenchmarkResult()
            self._benchmark_ordering(ordering)
            self._benchmark_construction(ordering)
            self._benchmark_minimising(ordering)
            self._analyse_bdd(ordering)
            self._analyse_min_bdd(ordering)

    def _benchmark_ordering(self, ordering):
        """
        Benchmarks the ordering phase of the BDD creation.
        :param ordering: The ordering to benchmark.
        """
        start_time = time()
        var_ordering = ordering.order_variables(self._fault_tree)
        self._results[ordering].ordering_time = time() - start_time
        self._results[ordering].ordering = var_ordering

    def _benchmark_construction(self, ordering):
        """
        Benchmarks the construction phase of the BDD creation.
        :param ordering: The ordering to benchmark.
        """
        var_order = self._results[ordering].ordering
        start_time = time()
        constructor = BDDConstructor(self._fault_tree)
        bdd = constructor.construct_bdd_test(var_order)
        self._results[ordering].construction_time = time() - start_time
        self._results[ordering].bdd = bdd

    def _benchmark_minimising(self, ordering):
        """
        Benchmark the minimising phase of the BDD creation.
        :param ordering: The ordering to benchmark.
        """
        bdd = self._results[ordering].bdd
        start_time = time()
        min_bdd = BDDMinimiser(bdd).minimise()
        self._results[ordering].minimising_time = time() - start_time
        self._results[ordering].min_bdd = min_bdd

    def _analyse_bdd(self, ordering):
        """
        Analyses the non minimised BDD.
        :param ordering: The ordering to analyse.
        """
        bdd = self._results[ordering].bdd
        bdd_analyser = BDDAnalyser(bdd)
        self._results[ordering].bdd_nodes = bdd_analyser.number_nodes()

    def _analyse_min_bdd(self, ordering):
        """
        Analyses the minimised BDD.
        :param ordering: The ordering to analyse.
        """
        bdd = self._results[ordering].min_bdd
        bdd_analyser = BDDAnalyser(bdd)
        number_nodes = bdd_analyser.number_nodes()
        self._results[ordering].min_bdd_nodes = number_nodes

    def __str__(self):
        """
        The string respresentation of the Benchmark.
        This shows, for each ordering, the name and the result.
        """
        r = ''
        for ordering, result in self._results.items():
            r += ordering.get_ordering_type() + '\n'
            r += str(result) + '\n'
            r += '------------------------------\n'
        return r

    def save_figure(self, path, dpi=100):
        """
        Saves a figure containing all the data from the analysis.
        This is done using the BDDBenchmarkGrapher class with
        matplotlib.
        :param path: The path to store the graph.
        :param dpi: The desired dpi of the image.
        """
        grapher = BDDBenchmarkGrapher(self._results, self._name)
        grapher.save_figure(path, dpi)


class BDDBenchmarkGrapher:
    """
    The BDDBenchmarkGrapher is used to graph the results from a
    BDDBenchmark class.
    """

    def __init__(self, results, name):
        """
        Constructor for a grapher class. It takes both the filled results
        from the BDDBenchmark class and a name to show as the plot title.
        :param results: A result dictionary from the BDDBenchmark class.
        :param name: The name of the analysed fault tree.
        """
        self._results = results
        self._bdd_nodes, self._min_bdd_nodes = [], []
        self._ord_times, self._con_times, self._min_times = [], [], []
        self._xticks = []
        self._indices = list(range(len(results)))
        self._name = name
        self._load_data()
        self._draw_results()

    @staticmethod
    def save_figure(path, dpi=100):
        """
        Saves the figure with the given path and dpi.
        :param path: The path where the image should be saved.
        :param dpi: The dpi in which the image should be saved.
        """
        plt.tight_layout()
        plt.savefig(path, dpi=dpi)

    def _load_data(self):
        """
        Load the data from the results dictionary in lists to ease the
        plotting of the data later.
        """
        for ordering, result in self._results.items():
            self._xticks.append(ordering.get_ordering_type())
            self._bdd_nodes.append(result.bdd_nodes)
            self._min_bdd_nodes.append(result.min_bdd_nodes)
            self._ord_times.append(result.ordering_time)
            self._con_times.append(result.construction_time)
            self._min_times.append(result.minimising_time)

    def _draw_results(self):
        """
        Draw all the results, this function calls a number of other
        functions that actually do the drawing.
        Here, we only create the axes and call the other functions
        with the axes.
        """
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        self._draw_bar_axes(ax1)
        self._draw_ticks_title(ax1)
        self._draw_times_axes(ax2)
        self._draw_legend(ax1, ax2)

    def _draw_bar_axes(self, axes):
        """
        Draws the bar graphs that describe the number of nodes of each
        result. We show two bars, the first one in the background that
        shows how many nodes there are in the unminimised BDD. And a
        second one showing how many nodes there are in the minimised BDD.
        :param axes: The axes to draw the bars on.
        """
        axes.set_ylabel('Number of nodes')
        axes.bar(self._indices, self._bdd_nodes, .25, align='center',
                 label='Unminimised nodes')
        axes.bar(self._indices, self._min_bdd_nodes, .25, align='edge',
                 label='Minimised nodes')

    def _draw_times_axes(self, axes):
        """
        Draws the time results of the benchmarks. This is done with three
        indicators, one red cross that shows the time taken to order the
        variables. One cyan circle that shows the time taken to construct
        the BDD and finally a black plus that shows the time taken to
        minimise the BDD.
        :param axes: The axes to draw the indicators on.
        """
        axes.set_ylabel('Time (s)')
        axes.plot(self._indices, self._ord_times, 'rx', alpha=.7, mew=5,
                  ms=10, label='Ordering time')
        axes.plot(self._indices, self._con_times, 'co', alpha=.7, mew=5,
                  ms=10, label='Construction time')
        axes.plot(self._indices, self._min_times, 'k+', alpha=.7, mew=5,
                  ms=10, label='Minimising time')

    def _draw_ticks_title(self, axes):
        """
        Draw the x ticks and the title of the graph.
        :param axes: The axes to draw the ticks on.
        """
        axes.tick_params(axis='x', rotation=12)
        plt.xticks(self._indices, self._xticks, rotation=45)
        plt.title('Results for {}'.format(self._name))

    @staticmethod
    def _draw_legend(axes1, axes2):
        """
        Draw the legend of the data of the two axes.
        We create one legend for all the data.
        :param axes1: The first axes.
        :param axes2: The second axes.
        """
        bars, barlabs = axes1.get_legend_handles_labels()
        times, timeslabs = axes2.get_legend_handles_labels()
        plt.legend(bars + times, barlabs + timeslabs, loc='best')
