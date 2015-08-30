__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '27 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

from graph.search import bfs


def edmonds_karp(flow_network):
    flow_network.reset_flows()

    get_path = lambda r: bfs(r, flow_network.source, flow_network.sink)
    residual = flow_network.get_residual_network()
    path = get_path(residual)
    while len(path):
        path_arcs = [(path[i], path[i+1]) for i in range(len(path)-1)]
        min_capacity = residual.get_arc_capacity(*min(path_arcs, key=lambda arc: residual.get_arc_capacity(*arc)))
        for (n1, n2) in path_arcs:
            try:
                flow_network.increase_flow(n1, n2, min_capacity)
            except ValueError:
                flow_network.decrease_flow(n1, n2, min_capacity)
        residual = flow_network.get_residual_network()
        path = get_path(residual)

    flows = {'flows': flow_network.flows,
             'max_flow': sum([v for (k, v) in flow_network.flows.items() if flow_network.source == k[0]])
             }

    return flows
