__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '08 September 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import time
import maxflow
import util
from graph.graph import DIMACSGraphFactory


def _measure_execution_time(func, *args):
    t1 = time.clock()
    func(*args)
    t2 = time.clock()
    return t2 - t1


def _run_maxflow(maxflow_func, data_file):
    flow_network = DIMACSGraphFactory.create(util.get_data_file(data_file))
    maxflow_func(flow_network)


def _run_by_density(density, maxflow_func):
    results = [_measure_execution_time(_run_maxflow, maxflow_func, '%s_%d.txt' % (density, i+1)) for i in range(200)]
    return results


def _run_batch(density):
    results = {
        'ek': _run_by_density(density, maxflow.edmonds_karp),
        'ff': _run_by_density(density, maxflow.ford_fulkerson),
        'cs': _run_by_density(density, maxflow.capacity_scaling),
        'pr': _run_by_density(density, maxflow.generic_push_relabel),
        'rf': _run_by_density(density, maxflow.relabel_to_front)
    }
    return results

if __name__ == '__main__':
    sparse_results = _run_batch('sparse')
    medium_results = _run_batch('medium')
    dense_results = _run_batch('dense')
