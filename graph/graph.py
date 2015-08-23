__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '23 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import itertools


class Graph(object):
    def __init__(self):
        self.nodes = {}

    def add_arc(self, n1, n2, c):
        self.nodes[(n1, n2)] = c

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
        g = Graph()

        with open(path_to_dimacs_file, 'r') as f:
            # problem descriptor
            (p, nodes, arcs) = f.readline().split(' ')
            g.total_nodes = int(nodes)
            g.total_arcs = int(arcs)
            # node descriptors
            (desc, n, t) = f.readline().split(' ')
            g.source = n
            (desc, n, t) = f.readline().split(' ')
            g.sink = n
            # arc descriptors
            for line in f.readline():
                (a, n1, n2, c) = line.split(' ')
                g.nodes[(n1, n2)] = c