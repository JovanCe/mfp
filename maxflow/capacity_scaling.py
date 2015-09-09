__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '05 September 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import math
from graph.search import bfs_min_capacity


def capacity_scaling(flow_network):
    max_capacity = sorted(flow_network.nodes.values()).pop()
    flow_network.reset()
    k = int(math.pow(2, math.floor(math.log(max_capacity, 2))))

    get_path = lambda delta: bfs_min_capacity(flow_network.residual, flow_network.source, flow_network.sink, k)
    path = get_path(k)
    while k >= 1:
        while len(path):
            path_arcs = [(path[i], path[i+1]) for i in range(len(path)-1)]
            for (n1, n2) in path_arcs:
                try:
                    flow_network.increase_flow(n1, n2, k)
                except KeyError:
                    flow_network.decrease_flow(n2, n1, k)

            path = get_path(k)

        k /= 2
        path = get_path(k)

    return flow_network.get_current_flows()
