__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '30 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

from collections import defaultdict


class PushRelabel(object):
    def __init__(self, flow_network):
        self.flow_network = flow_network
        self.height = {}
        self.excess = {}
        self._init_node_neighbour_lists()
        self.current_neighbhours = {k: 0 for k in flow_network.get_nodes()}

    def _init_node_neighbour_lists(self):
        all_neighbours = defaultdict(set)
        for n1, n2 in self.flow_network.nodes:
            all_neighbours[n1].add(n2)
            all_neighbours[n2].add(n1)

        self.all_neighbours = {k: list(v) for k, v in all_neighbours.items()}

    def _push(self, n1, n2):
        residual = self.flow_network.residual
        cf = residual.get_arc_capacity(n1, n2)
        if cf <= 0 or self.height[n1] != self.height[n2] + 1:
            return False

        delta_flow = min(self.excess[n1], cf)
        try:
            self.flow_network.increase_flow(n1, n2, delta_flow)
        except KeyError:
            self.flow_network.decrease_flow(n2, n1, delta_flow)
        self.excess[n1] -= delta_flow
        self.excess[n2] += delta_flow

        return True

    def _relabel(self, n):
        residual = self.flow_network.residual
        neighbours = residual.get_node_neighbours(n)
        min_neighbour_height = float('inf')

        for neighbour in neighbours:
            n_height = self.height[neighbour]

            if n_height < min_neighbour_height:
                min_neighbour_height = n_height
            if self.height[n] > n_height:
                return False

        self.height[n] = 1 + min_neighbour_height

        return True

    def _init_preflow(self):
        excess = {k: 0 for k in self.flow_network.get_nodes()}
        height = {k: 0 for k in self.flow_network.get_nodes()}
        self.flow_network.reset()
        s = self.flow_network.source
        height[s] = self.flow_network.total_nodes
        for n in self.flow_network.get_node_neighbours(s):
            c = self.flow_network.get_arc_capacity(s, n)
            self.flow_network.set_flow(s, n, c)
            excess[n] = c
            excess[s] -= c

        self.excess = excess
        self.height = height

    def _get_overflowing_node(self):
        for n, f in self.excess.items():
            if f > 0 and n != self.flow_network.source and n != self.flow_network.sink:
                return n

    def generic_push_relabel(self):
        self._init_preflow()

        node = self._get_overflowing_node()
        while node is not None:
            res = any([self._push(node, neighbour) for neighbour in self.flow_network.residual.get_node_neighbours(node)])
            if not res:
                self._relabel(node)

            node = self._get_overflowing_node()

        return self.flow_network.get_current_flows()

    def _discharge(self, n):
        i = self.current_neighbhours[n]
        neighbour_list = self.all_neighbours[n]
        while self.excess[n] > 0:
            try:
                neighbour = neighbour_list[i]
                success = self._push(n, neighbour)
                if not success:
                    i += 1
            except IndexError:
                self._relabel(n)
                i = 0
        self.current_neighbhours[n] = i

    def relabel_to_front(self):
        self._init_preflow()

        node_list = list(self.flow_network.get_nodes() - {self.flow_network.source, self.flow_network.sink})
        i = 0
        while True:
            try:
                n = node_list[i]
                old_height = self.height[n]
                self._discharge(n)
                if self.height[n] > old_height:
                    node_list.pop(i)
                    node_list.insert(0, n)
                    i = 0
                i += 1
            except IndexError:
                break

        return self.flow_network.get_current_flows()


def generic_push_relabel(flow_network):
    return PushRelabel(flow_network).generic_push_relabel()


def relabel_to_front(flow_network):
    return PushRelabel(flow_network).relabel_to_front()
