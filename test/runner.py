__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '29 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import sys
import maxflow
from graph import DIMACSGraphFactory
from test import get_data_file
from run_benchmark import measure_execution_time

if __name__ == '__main__':
    args = sys.argv
    test = args[1]

    test_mapping = {
        'ff': maxflow.ford_fulkerson,
        'ek': maxflow.edmonds_karp,
        'pr': maxflow.generic_push_relabel
    }

    graphs = []
    for i in range(5):
        graphs.append(DIMACSGraphFactory.create(get_data_file('dense_200.txt')))

    print 'pr: ' + str(maxflow.generic_push_relabel(graphs[0]))
    print 'rt: ' + str(maxflow.relabel_to_front(graphs[1]))
    print 'ff: ' + str(maxflow.ford_fulkerson(graphs[2]))
    print 'ek: ' + str(maxflow.edmonds_karp(graphs[3]))
    print 'cs: ' + str(maxflow.capacity_scaling(graphs[4]))
    
    print 'pr: ' + str(measure_execution_time(maxflow.generic_push_relabel, graphs[0]))
    print 'rt: ' + str(measure_execution_time(maxflow.relabel_to_front, graphs[1]))
    print 'ff: ' + str(measure_execution_time(maxflow.ford_fulkerson, graphs[2]))
    print 'ek: ' + str(measure_execution_time(maxflow.edmonds_karp, graphs[3]))
    print 'cs: ' + str(measure_execution_time(maxflow.capacity_scaling, graphs[4]))