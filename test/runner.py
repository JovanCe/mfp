__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '29 August 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import sys
import max

if __name__ == '__main__':
    args = sys.argv
    test = args[1]

    test_mapping = {
        'ff': max.test_ford_fulkerson
    }

    test_mapping[test]()