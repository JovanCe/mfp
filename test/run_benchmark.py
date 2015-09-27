__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '08 September 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import time
import json
import maxflow
import util
from graph.graph import DIMACSGraphFactory


def measure_execution_time(func, *args):
    t1 = time.clock()
    func(*args)
    t2 = time.clock()
    return t2 - t1


def _run_maxflow(maxflow_func, data_file):
    flow_network = DIMACSGraphFactory.create(util.get_data_file(data_file))
    return measure_execution_time(maxflow_func, flow_network)


def _run_by_density(density, maxflow_func):
    results = [_run_maxflow(maxflow_func, '%s_%d.txt' % (density, i+1)) for i in range(200)]
    return results


def _run_batch(density):
    results = {
        'ek': _run_by_density(density, maxflow.edmonds_karp),
        'df': _run_by_density(density, maxflow.edmonds_karp_dfs),
        'ff': _run_by_density(density, maxflow.ford_fulkerson),
        'pq': _run_by_density(density, maxflow.ford_fulkerson_pq),
        'cs': _run_by_density(density, maxflow.capacity_scaling),
        'pr': _run_by_density(density, maxflow.generic_push_relabel),
        'rf': _run_by_density(density, maxflow.relabel_to_front)
    }
    return results

if __name__ == '__main__':
    sparse_results = _run_batch('sparse')
    with open(util.get_out_file('sparse.txt'), 'w') as f:
        json.dump(sparse_results, f)

    medium_results = _run_batch('medium')
    with open(util.get_out_file('medium.txt'), 'w') as f:
        json.dump(medium_results, f)

    dense_results = _run_batch('dense')
    with open(util.get_out_file('dense.txt'), 'w') as f:
        json.dump(dense_results, f)

