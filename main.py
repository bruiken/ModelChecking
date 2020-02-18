from faulttree import BasicEvent, AndGate, OrGate, FaultTree
from bdd import BDDConstructor


if __name__ == '__main__':
    base_events = {x: BasicEvent(str(x)) for x in range(1, 9)}
    gates = OrGate('SYSTEM', [
        OrGate('LEFT', [
            base_events[1],
            base_events[2]
        ]),
        AndGate('MIDDLE', [
            base_events[3],
            base_events[4],
            base_events[5]
        ]),
        OrGate('RIGHT', [
            base_events[6],
            AndGate('RIGHT_AND', [
                base_events[7],
                base_events[8]
            ])
        ])
    ])
    fault_tree = FaultTree('Tree 1', base_events, gates)
    bdd_constructor = BDDConstructor(fault_tree)
    bdd = bdd_constructor.construct_bdd([1, 2, 6, 7, 8, 3, 4, 5], fault_tree.get_false_state())
    print(bdd)
