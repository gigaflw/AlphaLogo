# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-01 21:04:27
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-02 10:32:31

# Images in this path will be indexed
import os

INDEX_BASE_DIR = os.path.join(os.path.dirname(__file__), 'index')
IMAGE_MIRROR_DIR = os.path.join(INDEX_BASE_DIR, 'images')

LUCENE_INDEX_DIR = os.path.join(INDEX_BASE_DIR, 'web.index')
LUCENE_CATELOG_FILE = os.path.join(INDEX_BASE_DIR, 'web.index', 'PICTURES.txt')

COLOR_SLOTS = 8
COLOR_LEVEL = 8
