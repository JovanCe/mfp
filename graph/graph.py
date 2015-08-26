__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '23 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import itertools


class FlowNetwork(object):
    def __init__(self, source, sink):
        self.source = source
        self.sink = sink
        self.nodes = {}
        self.flows = {}

    def add_arc(self, n1, n2, c):
        self.nodes[(n1, n2)] = c
        self.flows[(n1, n2)] = 0

    def get_nodes(self):
        return set(itertools.chain.from_iterable(self.nodes.keys()))

    def get_arc_capacity(self, n1, n2):
        return self.nodes[(n1, n2)]

    def get_node_neighbours(self, n):
        neighbours = []
        for (n1, n2) in self.nodes.keys():
            if n == n1:
                neighbours.append(n2)
        return neighbours

    def get_residual_network(self):
        r = FlowNetwork(self.source, self.sink)
        r.source = self.source
        r.sink = self.sink
        for (n1, n2), c in self.nodes.items():
            flow = self.flows[(n1, n2)]
            if flow > 0:
                r.add_arc(n2, n1, flow)
            r.add_arc(n1, n2, c-flow)
        return r


class DIMACSGraphFactory(object):
    @classmethod
    def create(cls, path_to_dimacs_file):
        with open(path_to_dimacs_file, 'r') as f:
            # problem descriptor
            (nodes, arcs) = f.readline().split(' ')[2:]
            total_nodes = int(nodes)
            total_arcs = int(arcs)
            # node descriptors
            n = int(f.readline().split(' ')[1:][0])
            m = int(f.readline().split(' ')[1:][0])
            g = FlowNetwork(n, m)
            g.total_nodes = total_nodes

            # arc descriptors
            for line in f:
                (n1, n2, c) = line.split(' ')[1:]
                # ignore incoming edges to source and outgoing from sink
                if n1 == m or n2 == n:
                    total_arcs -= 1
                    continue
                g.add_arc(int(n1), int(n2), int(c.strip()))
            g.total_arcs = total_arcs
        return g