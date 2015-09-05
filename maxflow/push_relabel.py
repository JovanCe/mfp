__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '30 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

from collections import defaultdict


def _push(flow_network, n1, n2, excess, height):
    residual = flow_network.get_residual_network()
    if residual.get_arc_capacity(n1, n2) <= 0 or height[n1] != height[n2] + 1:
        return False

    delta_flow = min(excess[n1], residual.get_arc_capacity(n1, n2))
    try:
        flow_network.increase_flow(n1, n2, delta_flow)
    except KeyError:
        flow_network.decrease_flow(n2, n1, delta_flow)
    excess[n1] -= delta_flow
    excess[n2] += delta_flow

    return True


def _relabel(flow_network, n, height):
    residual = flow_network.get_residual_network()

    for neighbour in residual.get_node_neighbours(n):
        if height[n] > height[neighbour]:
            return False

    height[n] = 1 + min([height[neighbour] for neighbour in residual.get_node_neighbours(n)])

    return True


def _init_preflow(flow_network):
    excess = {k: 0 for k in flow_network.get_nodes()}
    height = {k: 0 for k in flow_network.get_nodes()}
    flow_network.reset_flows()
    s = flow_network.source
    height[s] = flow_network.total_nodes
    for n in flow_network.get_node_neighbours(s):
        c = flow_network.get_arc_capacity(s, n)
        flow_network.set_flow(s, n, c)
        excess[n] = c
        excess[s] -= c

    return excess, height


def _get_overflowing_node(flow_network, excess):
    for n, f in excess.items():
        if f > 0 and n != flow_network.source and n != flow_network.sink:
            return n


def generic_push_relabel(flow_network):
    excess, height = _init_preflow(flow_network)

    node = _get_overflowing_node(flow_network, excess)
    while node is not None:
        res = any([_push(flow_network, node, neighbour, excess, height) for neighbour in flow_network.get_residual_network().get_node_neighbours(node)])
        if not res:
            _relabel(flow_network, node, height)

        node = _get_overflowing_node(flow_network, excess)

    return flow_network.get_current_flows()


def _get_node_neighbour_lists(flow_network):
    all_neighbours = defaultdict(set)
    for n1, n2 in flow_network.nodes:
        all_neighbours[n1].add(n2)
        all_neighbours[n2].add(n1)

    return {k: list(v) for k, v in all_neighbours.items()}


def _discharge(flow_network, node, neighbour_list, excess, height):
    i = 0
    while excess[node] > 0:
        try:
            n = neighbour_list[i]
            success = _push(flow_network, node, n, excess, height)
            if not success:
                i += 1
        except IndexError:
            _relabel(flow_network, node, height)
            i = 0


def relabel_to_front(flow_network):
    excess, height = _init_preflow(flow_network)
    all_neighbours = _get_node_neighbour_lists(flow_network)
    node_list = list(flow_network.get_nodes() - {flow_network.source, flow_network.sink})
    i = 0
    while True:
        try:
            n = node_list[i]
            old_height = height[n]
            _discharge(flow_network, n, all_neighbours[n], excess, height)
            if height[n] > old_height:
                node_list.pop(i)
                node_list.insert(0, n)
                i = 0
            i += 1
        except IndexError:
            break

    return flow_network.get_current_flows()


