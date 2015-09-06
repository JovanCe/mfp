__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '23 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

from Queue import Queue


def bfs(graph, source, target):
    """
    Finds a path from source to target using breadth-first search
    :param graph:
    :param source:
    :param target:
    :return:
    """
    nodes = graph.get_nodes()
    queue = Queue(len(nodes))
    distances = {}
    parents = {}
    for n in nodes:
        # infinite distance
        distances[n] = -1
        # no parent
        parents[n] = -1

    distances[source] = 0
    queue.put(source)
    while not queue.empty():
        u = queue.get()
        if u == target:
            path = []
            while parents[u] != -1:
                path.insert(0, u)
                u = parents[u]
            # check if a path exists and add the source node for complete path
            if len(path):
                path.insert(0, u)
            return path
        for n in graph.get_node_neighbours(u):
            if distances[n] == -1:
                distances[n] = distances[u] + 1
                parents[n] = u
                queue.put(n)

    return []


def bfs_min_capacity(flow_network, source, target, min_capacity):
    """
    Finds a path from source to target using breadth-first search
    :param graph:
    :param source:
    :param target:
    :return:
    """
    nodes = flow_network.get_nodes()
    queue = Queue(len(nodes))
    distances = {}
    parents = {}
    for n in nodes:
        # infinite distance
        distances[n] = -1
        # no parent
        parents[n] = -1

    distances[source] = 0
    queue.put(source)
    while not queue.empty():
        u = queue.get()
        if u == target:
            path = []
            while parents[u] != -1:
                path.insert(0, u)
                u = parents[u]
            # check if a path exists and add the source node for complete path
            if len(path):
                path.insert(0, u)
            return path
        for n in flow_network.get_node_neighbours(u):
            if distances[n] == -1 and flow_network.get_arc_capacity(u, n) >= min_capacity:
                distances[n] = distances[u] + 1
                parents[n] = u
                queue.put(n)

    return []

def dfs(graph, node):
    pass


