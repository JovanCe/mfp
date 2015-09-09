__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '27 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

from graph.search import bfs


def edmonds_karp(flow_network):
    flow_network.reset()

    get_path = lambda: bfs(flow_network.residual, flow_network.source, flow_network.sink)
    path = get_path()
    while len(path):
        path_arcs = [(path[i], path[i+1]) for i in range(len(path)-1)]
        min_capacity = flow_network.residual.get_arc_capacity(
            *min(path_arcs, key=lambda arc: flow_network.residual.get_arc_capacity(*arc)))

        for (n1, n2) in path_arcs:
            try:
                flow_network.increase_flow(n1, n2, min_capacity)
            except KeyError:
                flow_network.decrease_flow(n2, n1, min_capacity)

        path = get_path()

    return flow_network.get_current_flows()
