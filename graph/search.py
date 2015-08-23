__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '23 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

from Queue import Queue


def bfs(graph, node):
    nodes = graph.get_nodes()
    queue = Queue(len(nodes))
    distances = {}
    parents = {}
    for n in nodes:
        # infinite distance
        distances[n] = -1
        # no parent
        parents[n] = -1

    distances[node] = 0
    while not queue.empty():
        u = queue.get()
        for n in graph.get_neighbours(u):
            if distances[n] == -1:
                distances[n] = distances[u] + 1
            parents[n] = u
            queue.put(n)

    return distances


