from faulttree.readers import GalileoReader
from prettyprinting import PrettyPrintFaultTree


if __name__ == '__main__':
    reader = GalileoReader(r'.\input.dft')  # galileo file input
    ft = reader.create_faulttree()
    PrettyPrintFaultTree(ft).print_to_window()
