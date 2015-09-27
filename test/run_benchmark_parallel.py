__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '26 September 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import multiprocessing
import time
import json
import maxflow
import util
from graph.graph import DIMACSGraphFactory


class Worker(object):
    def __init__(self, density, batch_size):
        self._density = density
        self._batch_size = batch_size

    def measure_execution_time(self, func, *args):
        t1 = time.clock()
        func(*args)
        t2 = time.clock()
        return t2 - t1

    def _run_maxflow(self, maxflow_func, data_file):
        flow_network = DIMACSGraphFactory.create(util.get_data_file(data_file))
        return self.measure_execution_time(maxflow_func, flow_network)

    def _run_by_density(self, maxflow_func):
        results = [self._run_maxflow(maxflow_func, '%s_%d.txt' % (self._density, i))
                   for i in range(self._start, self._start + self._batch_size)]
        return results

    def _run_batch(self):
        results = {
            'ek': self._run_by_density(maxflow.edmonds_karp),
            'df': self._run_by_density(maxflow.edmonds_karp_dfs),
            'ff': self._run_by_density(maxflow.ford_fulkerson),
            'pq': self._run_by_density(maxflow.ford_fulkerson_pq),
            'cs': self._run_by_density(maxflow.capacity_scaling),
            'pr': self._run_by_density(maxflow.generic_push_relabel),
            'rf': self._run_by_density(maxflow.relabel_to_front)
        }
        return results

    def __call__(self, ord):
        self._ord = ord + 1
        self._start = ord * self._batch_size + 1
        results = self._run_batch()
        with open(util.get_out_file('worker', 'sparse_%d.txt' % self._ord), 'w') as f:
            json.dump(results, f)

        print "WORKER %d DONE" % self._ord


def _execute(density):
    num_process = 10
    batch_size = 20
    pool = multiprocessing.Pool(processes=num_process)
    pool.map(Worker(density, batch_size), range(num_process))
    pool.close()
    pool.join()

    results = {
        'ff': [],
        'pq': [],
        'ek': [],
        'df': [],
        'cs': [],
        'pr': [],
        'rf': []
    }
    for i in range(num_process):
        res = json.load(open(util.get_out_file('worker', '%s_%d.txt' % (density, i+1))))
        for k, v in res.items():
            results[k].extend(v)
    with open(util.get_out_file('%s.txt' % density), 'w') as f:
        json.dump(results, f)

    print '%s DONE' % density.upper()


if __name__ == '__main__':
    _execute('sparse')
    _execute('medium')
    _execute('dense')