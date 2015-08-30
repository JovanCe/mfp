__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '29 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import sys
import maxflow
from graph import DIMACSGraphFactory
from test import get_data_file

if __name__ == '__main__':
    args = sys.argv
    test = args[1]

    test_mapping = {
        'ff': maxflow.ford_fulkerson,
        'ek': maxflow.edmonds_karp
    }

    graph = DIMACSGraphFactory.create(get_data_file('2.txt'))
    flows = test_mapping[test](graph)
    print flows
