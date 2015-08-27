__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '27 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

from graph.shortest_path import dijkstra


def ford_fulkerson(flow_network):
    flow_network.reset_flows()

    get_path = lambda residual: dijkstra(residual, flow_network.source, flow_network.sink)
    residual = flow_network.get_residual_network()
    path = get_path(residual)
    while len(path):
        path_arcs = [(path[i], path[i+1]) for i in range(len(path)-1)]
        min_flow = residual.get_arc_capacity(*min(path_arcs, key=lambda arc: residual.get_arc_capacity(*arc)))
        for (n1, n2) in path_arcs:
            try:
                flow_network.increase_flow(n1, n2, min_flow)
            except ValueError:
                flow_network.decrease_flow(n1, n2, min_flow)
        residual = flow_network.get_residual_network()
        path = get_path(residual)

    return flow_network.flows