from builtins import str
from builtins import object
import pygraphviz as pgv


class Visualizer(object):

    def __init__(self):
        self._added = set()

    def draw(self, filename, kwtree):
        g = pgv.AGraph(directed=True)
        for state in kwtree._states:
            if state['success']:
                g.add_node(
                    state['id'], color='green',
                    label=str(state['id']) + ' [' +
                    state['matched_keyword'] + ']')
            else:
                g.add_node(state['id'])
        for state in kwtree._states:
            if 'transitions' in state:
                for symbol_id, state_id in enumerate(state['transitions']):
                    if state_id >= 0:
                        g.add_edge(state['id'], state_id,
                                   label=kwtree._symbol_list[symbol_id])
        g.draw(filename, prog='dot')
