__author__ = 'Jovan Cejovic <jovan.cejovic@sbgenomics.com>'
__date__ = '07 September 2015'
__copyright__ = 'Copyright (c) 2015 Seven Bridges Genomics'

import os

DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
OUT_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'out')


def get_data_file(filename):
    return os.path.join(DATA_DIR, filename)


def get_out_file(*paths):
    return os.path.join(OUT_DIR, *paths)