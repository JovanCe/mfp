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


def generate(num_nodes, num_arcs, density='sparse', problem_num=1):
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
    :param problem_num: the current problem number, used for generating output file name
    :return:
    """
    seed = int(time.mktime(datetime.utcnow().timetuple()))
    args = [seed, problem_num, num_nodes, 1, 1, num_arcs, 1, 1, 1, 0, 0, 0, 100, 10, 100]

    netgen_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'lib', 'netgen', 'bin', 'netgen.out')
    netgen = Popen(netgen_path, stdin=PIPE, stdout=PIPE)
    out, err = netgen.communicate(" ".join([str(arg) for arg in args]))
    _save_to_file(out, problem_num, density)


def _generate_node_arc_num(density, k):
    narcs = []
    for i in range(k):
        nodes = random.randint(200, 1000)
        arcs = _arcs_num_by_density(density, nodes)
        narcs.append((nodes, arcs))

    return sorted(narcs)


def _arcs_num_by_density(density_level, num_nodes):
    def get_arcs(density):
        return int(math.floor(density * num_nodes * (num_nodes - 1)))
    if density_level == 'sparse':
        return get_arcs(random.uniform(0.1, 0.3))
    elif density_level == 'medium':
        return get_arcs(random.uniform(0.4, 0.6))
    elif density_level == 'dense':
        return get_arcs(random.uniform(0.7, 1.0))


def _save_to_file(netgen_output, problem_num, density):
    with open(util.get_data_file('%s_%d.txt' % (density, problem_num)), 'w') as f:
        nl = ''
        for line in netgen_output.split('\n'):
            if not line.replace('\n', '') or line.startswith('c'):
                continue
            f.write('%s%s' % (nl, line))
            nl = '\n'


if __name__ == '__main__':
    i = 0
    for nodes, arcs in _generate_node_arc_num('sparse', 200):
        generate(nodes, arcs, 'sparse', i+1)
        i += 1

    i = 0
    for nodes, arcs in _generate_node_arc_num('medium', 200):
        generate(nodes, arcs, 'medium', i+1)
        i += 1

    i = 0
    for nodes, arcs in _generate_node_arc_num('dense', 200):
        generate(nodes, arcs, 'dense', i+1)
        i += 1
