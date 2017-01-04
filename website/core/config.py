# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-01 21:04:27
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-04 14:20:33

# Images in this path will be indexed
import os

INDEX_BASE_DIR = os.path.join(os.path.dirname(__file__), 'index')
IMAGE_MIRROR_DIR = os.path.join(INDEX_BASE_DIR, 'images')

LUCENE_INDEX_DIR = os.path.join(INDEX_BASE_DIR, 'web.index')
LUCENE_CATELOG_FILE = os.path.join(INDEX_BASE_DIR, 'web.index', 'PICTURES.txt')

FILE_FIELD_FORMAT = ["ind", "ent_name", "info", "keywords", "imgurl", "filename", "url"]
STORE_FIELDS = ["ind", "filename", "ent_name", "info", "theme_colors"]
INDEX_FIELDS = ["ent_name", "keywords", "n_colors"]
ADD_FIELDS = STORE_FIELDS + INDEX_FIELDS

COLOR_SLOTS = 8
COLOR_LEVEL = 8

# Delayed import is necessary to avoid cyclic import
from website.core.index.utility import theme_colors_for_web
FIELD_FUNCS = {
    "filename" : lambda f:"{:05d}".format(int(f['ind'])) + '.jpg',
    "keywords" : lambda f:f['keywords'].replace('%', ' '),
    "theme_colors" : lambda f:" ".join(theme_colors_for_web(f['filename'])),
    "n_colors" : lambda f:str(f['theme_colors'].count(' ') + 1)
}

