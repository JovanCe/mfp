__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '23 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import itertools


class FlowNetwork(object):
    def __init__(self):
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


class DIMACSGraphFactory(object):
    @classmethod
    def create(cls, path_to_dimacs_file):
        g = FlowNetwork()

        with open(path_to_dimacs_file, 'r') as f:
            # problem descriptor
            (nodes, arcs) = f.readline().split(' ')[2:]
            g.total_nodes = int(nodes)
            g.total_arcs = int(arcs)
            # node descriptors
            (n, t) = f.readline().split(' ')[1:]
            g.source = int(n)
            (n, t) = f.readline().split(' ')[1:]
            g.sink = int(n)
            # arc descriptors
            for line in f:
                (n1, n2, c) = line.split(' ')[1:]
                g.add_arc(int(n1), int(n2), int(c.strip()))
        return g