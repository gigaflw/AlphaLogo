# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-01 21:04:27
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-04 16:07:08

# Images in this path will be indexed
import os

INDEX_BASE_DIR = os.path.join(os.path.dirname(__file__), 'index')

LUCENE_INDEX_DIR = os.path.join(INDEX_BASE_DIR, 'web.index')
LUCENE_CATELOG_FILE = os.path.join(INDEX_BASE_DIR, 'web.index', 'PICTURES.txt')
IMAGE_INDEX_DIR = os.path.join(INDEX_BASE_DIR, 'image.index')
IMAGE_INDEX_PKL_FILE = os.path.join(IMAGE_INDEX_DIR, 'lsh.pkl')

COLOR_SLOTS = 8
COLOR_LEVEL = 8

