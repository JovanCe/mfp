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
        self.total_nodes = self.total_arcs = 0

    def add_arc(self, n1, n2, c):
        """
        Adds a directed arc
        :param n1: starting node
        :param n2: ending node
        :param c: capacity of the arc
        :return:
        """
        self.nodes[(n1, n2)] = c
        self.flows[(n1, n2)] = 0

    def set_flow(self, n1, n2, f):
        """
        Sets the flow for an arc denoted by starting and ending node
        :param n1: starting arc node
        :param n2: ending arc node
        :param f: flow value
        :return:
        """
        if (n1, n2) in self.nodes:
            self.flows[(n1, n2)] = f
        else:
            raise ValueError('Arc (%d, %d) doesn\'t exist', (n1, n2))

    def increase_flow(self, n1, n2, f):
        """
        Increases the arc flow by value f
        :param n1: starting arc node
        :param n2: ending arc node
        :param f: value by which to increase
        :return:
        """
        self.set_flow(n1, n2, self.flows[(n1, n2)] + f)

    def decrease_flow(self, n1, n2, f):
        """
        Decrease the arc flow by value f
        :param n1: starting arc node
        :param n2: ending arc node
        :param f: value by which to decrease
        :return:
        """
        self.set_flow(n1, n2, self.flows[(n1, n2)] - f)

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

    def reset_flows(self):
        self.flows = {k: 0 for k in self.nodes.keys()}

    @property
    def density(self):
        if self.total_nodes == 0:
            return 0
        return float(self.total_arcs) / (self.total_nodes * (self.total_nodes - 1))


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