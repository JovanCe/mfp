__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '23 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

from collections import defaultdict


class FlowNetwork(object):
    def __init__(self, source, sink, residual=False, node_set=None):
        self._source = source
        self._sink = sink
        self._nodes = {}
        self._flows = {}
        self.total_nodes = self.total_arcs = 0
        self._residual = None
        self._neighbours = defaultdict(set)
        self._node_set = node_set
        if not residual:
            self._residual = FlowNetwork(self.source, self.sink, True)

    def add_arc(self, n1, n2, c):
        """
        Adds a directed arc
        :param n1: starting node
        :param n2: ending node
        :param c: capacity of the arc
        :return:
        """
        self._nodes[(n1, n2)] = c
        self._flows[(n1, n2)] = 0
        self._neighbours[n1].add(n2)
        if self._residual:
            self._residual.add_arc(n1, n2, c)

    def remove_arc(self, n1, n2):
        if self._nodes.get((n1, n2), None) is not None:
            del self._nodes[(n1, n2)]
            self._neighbours[n1].remove(n2)

    def set_flow(self, n1, n2, f):
        """
        Sets the flow for an arc denoted by starting and ending nodes
        :param n1: starting arc node
        :param n2: ending arc node
        :param f: flow value
        :return:
        """
        self._flows[(n1, n2)] = f
        if self._residual:
            c = self.nodes[(n1, n2)]
            if f > 0:
                self._residual.add_arc(n2, n1, f)
            else:
                self._residual.remove_arc(n2, n1)
            if c-f > 0:
                self._residual.add_arc(n1, n2, c-f)
            else:
                self._residual.remove_arc(n1, n2)

    def increase_flow(self, n1, n2, f):
        """
        Increases the arc flow by value f
        :param n1: starting arc node
        :param n2: ending arc node
        :param f: value by which to increase
        :return:
        """
        self.set_flow(n1, n2, self._flows[(n1, n2)] + f)

    def decrease_flow(self, n1, n2, f):
        """
        Decrease the arc flow by value f
        :param n1: starting arc node
        :param n2: ending arc node
        :param f: value by which to decrease
        :return:
        """
        self.set_flow(n1, n2, self._flows[(n1, n2)] - f)

    def get_arc_capacity(self, n1, n2):
        try:
            return self._nodes[(n1, n2)]
        except KeyError:
            return 0

    def get_node_neighbours(self, n):
        """
        Returns a list of adjacent nodes (respecting edge directions) for a given node
        :param n: desired node
        :return:
        """
        return list(self._neighbours[n])

    def reset(self):
        self._flows = {k: 0 for k in self._nodes.keys()}
        if self._residual:
            self._residual._nodes = {}
            self._residual._neighbours = defaultdict(set)
            for (n1, n2), c in self._nodes.items():
                self._residual.add_arc(n1, n2, c)

    def get_current_flows(self):
        return {
            'flows': self.flows,
            'max_flow': sum([v for (k, v) in self.flows.items() if self.source == k[0]]),
            }

    @property
    def density(self):
        if self.total_nodes == 0:
            return 0
        return float(self.total_arcs) / (self.total_nodes * (self.total_nodes - 1))

    @property
    def flows(self):
        return self._flows

    @property
    def nodes(self):
        return self._nodes

    @property
    def source(self):
        return self._source

    @property
    def sink(self):
        return self._sink

    @property
    def residual(self):
        return self._residual

    @property
    def node_set(self):
        """
        Return a set of all the nodes in the flow network
        :return:
        """
        return self._node_set

    @node_set.setter
    def node_set(self, node_set):
        self._node_set = node_set


class DIMACSGraphFactory(object):
    """
    Constructs flow networks by parsing files with graph information in DIMACS format.
    """
    @classmethod
    def create(cls, path_to_dimacs_file):
        with open(path_to_dimacs_file, 'r') as f:
            # problem descriptor
            (nodes, arcs) = f.readline().split(' ')[2:]
            total_nodes = int(nodes)
            total_arcs = int(arcs)
            # node descriptors
            s = int(f.readline().split(' ')[1:][0])
            t = int(f.readline().split(' ')[1:][0])
            g = FlowNetwork(s, t)
            g.total_nodes = total_nodes

            # arc descriptors
            nodes = set()
            for line in f:
                (n1, n2, c) = [int(i) for i in line.split(' ')[1:]]
                # ignore incoming edges to source and outgoing from sink
                if n1 == t or n2 == s or n2 == 0:
                    total_arcs -= 1
                    continue
                g.add_arc(n1, n2, c)
                nodes.add(n1)
                nodes.add(n2)
            g.total_arcs = total_arcs
            g.node_set = nodes
            g.residual.node_set = nodes
        return g