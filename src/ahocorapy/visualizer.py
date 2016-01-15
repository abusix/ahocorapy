import pygraphviz as pgv


class Visualizer:

    def __init__(self):
        self._added = set()

    def draw(self, filename, kwtree):
        g = pgv.AGraph(directed=True)
        for state in kwtree._states:
            g.add_node(str(state['id']))
        for state in kwtree._states:
            if 'transitions' in state:
                for symbol_id, state_id in enumerate(state['transitions']):
                    if state_id >= 0:
                        g.add_edge(str(state['id']), str(state_id),
                                   label=kwtree._symbol_list[symbol_id])
        g.draw(filename, prog='dot')
