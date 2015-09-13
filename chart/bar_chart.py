__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '13 September 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import numpy as np
import matplotlib.pyplot as plt
import util


def draw_bar(means, density):
    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})

    ind = np.arange(len(means))  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects = ax.bar(ind, means, width, color='g')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Milliseconds')
    ax.set_title('Average running time on %s networks' % density)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(('Ford-Fulkerson', 'Edmonds-Karp', 'Capacity scaling', 'Generic push relabel', 'Relabel to front'),
                       rotation=40, ha='right', fontsize=10)

    def autolabel(rects):
        # attach some text labels
        for i, rect in enumerate(rects):
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., height + 0.05, '%d' % means[i],
                    ha='center', va='bottom')

    autolabel(rects)

    plt.savefig(util.get_out_file('chart', '%s.png' % density))

if __name__ == '__main__':
    draw_bar((1,2,3,4,5), 'sparse')