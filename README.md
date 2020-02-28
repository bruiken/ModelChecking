# ModelChecking

## Pretty Printing
### Required packages
 - networkx
 - matplotlib
 - pygraphviz (on Windows this is easiest by using Anaconda or MiniConda)

### Definition
Trees defined here are pretty printable. To do so, use the `PrettyPrintFaultTree` or, in the future, the `PrettyPrintBDD` class. These classes are based on an abstract `_PrettyPrint` class. The only use for the abstract class is to define the functions `print_to_window` and `print_to_file`. These functions print the result to a window or to a file respectively. This is done by calling the related `matplotlib` functions. This means that the actual functions that prepare the graphs for printing should prepare the results using `matplotlib`. This is what the `_pretty_print` function should do. 
