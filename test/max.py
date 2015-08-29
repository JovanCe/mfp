__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '29 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

from test import get_data_file
from graph import FlowNetwork, DIMACSGraphFactory
from maxflow import ford_fulkerson


def test_ford_fulkerson():
    graph = DIMACSGraphFactory.create(get_data_file('1.txt'))
    flows = ford_fulkerson(graph)
    print flows
