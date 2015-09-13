__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '14 September 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import util
import json
from bar_chart import draw_bar


def _prepare_data(density):
    data = util.get_out_file('%s.txt' % density)

    d = {}
    with open(data, 'r') as f:
        d = json.load(f)

    results = {}
    for k, v in d.items():
        mean = sum(v) / 200.0
        results[k] = mean * 1000

    return results['ff'], results['ek'], results['cs'], results['pr'], results['rf']

if __name__ == '__main__':
    draw_bar(_prepare_data('sparse'), 'sparse')
    draw_bar(_prepare_data('medium'), 'medium')
    draw_bar(_prepare_data('dense'), 'dense')