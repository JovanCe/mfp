__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '27 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'


def dijkstra(graph, source, target):
    """
    Returns the shortest path from source to the target node
    :param graph:
    :param source:
    :param target:
    :return:
    """
    dist = {source: 0}
    prev = {source: -1}
    nodes = graph.get_nodes()
    q = []

    for node in nodes:
        if node != source:
            dist[node] = float('inf')
            prev[node] = -1
        q.append(node)

    while len(q):
        q.sort(key=lambda x: dist[x], reverse=True)
        node = q.pop()
        if node == target:
            path = []
            while prev[node] != -1:
                path.insert(0, node)
                node = prev[node]
            return path

        for neighbour in graph.get_node_neighbours(node):
            alt = dist[node] + 1
            if alt < dist[neighbour]:
                dist[neighbour] = alt
                prev[neighbour] = node
