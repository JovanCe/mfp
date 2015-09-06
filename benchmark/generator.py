__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '01 September 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import os
import random
import math
from datetime import datetime
import time
from subprocess import Popen, PIPE

import util


def generate(density='sparse', problem_num=1):
    """
    Input generator for the netgen C library.
    Example input:
    c   Random seed:               98878
    c   Number of nodes:               4
    c   Source nodes:                  1
    c   Sink nodes:                    1
    c   Number of arcs:                4
    c   Minimum arc cost:              1
    c   Maximum arc cost:              1
    c   Total supply:                  1
    c   Transshipment -
    c     Sources:                     0
    c     Sinks:                       0
    c   Skeleton arcs -
    c     With max cost:               0%
    c     Capacitated:               100%
    c   Minimum arc capacity:          2
    c   Maximum arc capacity:          5
    :param density: sparse, medium or dense, determines the total number of arcs in regards to graph density
    :param problem_num: the current problem number, used for generating output file name
    :return:
    """
    seed = int(time.mktime(datetime.utcnow().timetuple()))
    random.seed(seed)
    num_nodes = random.randint(20, 50)
    num_arcs = _arcs_num_by_density(density, num_nodes)
    args = [seed, problem_num, num_nodes, 1, 1, num_arcs, 1, 1, 1, 0, 0, 0, 100, 10, 100]

    netgen_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'lib', 'netgen', 'bin', 'netgen.out')
    netgen = Popen(netgen_path, stdin=PIPE, stdout=PIPE)
    out, err = netgen.communicate(" ".join([str(arg) for arg in args]))
    _save_to_file(out, problem_num)


def _arcs_num_by_density(density_level, num_nodes):
    def get_arcs(density):
        return int(math.floor(density * num_nodes * (num_nodes - 1)))
    if density_level == 'sparse':
        return get_arcs(random.uniform(0.00001, 0.3))
    elif density_level == 'medium':
        return get_arcs(random.uniform(0.4, 0.6))
    elif density_level == 'dense':
        return get_arcs(random.uniform(0.7, 1.0))


def _save_to_file(netgen_output, problem_num):
    with open(util.get_data_file('%d.txt' % problem_num), 'w') as f:
        for line in netgen_output.split('\n'):
            if not line.replace('\n', '') or line.startswith('c'):
                continue
            f.write(line + '\n')


if __name__ == '__main__':
    generate('sparse', 10)
