# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-01 21:04:27
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-11 20:40:30

# Images in this path will be indexed
from website.config import DATABASE_DIR
import os

INDEX_BASE_DIR = DATABASE_DIR

LUCENE_INDEX_DIR = os.path.join(INDEX_BASE_DIR, 'web.index')
LUCENE_CATELOG_FILE = os.path.join(INDEX_BASE_DIR, 'PICTURES.txt')
IMAGE_INDEX_DIR = os.path.join(INDEX_BASE_DIR, 'image.index')
IMAGE_INDEX_PKL_FILE = os.path.join(IMAGE_INDEX_DIR, 'lsh.pkl')
IMAGE_INDEX_TTH_FILE = os.path.join(IMAGE_INDEX_DIR, 'tth.pkl')
IMAGE_INDEX_TTH_DATA_FILE = os.path.join(IMAGE_INDEX_DIR, 'tth.data.pkl')

N_COLORS_MORE_THAN_SIX = 0

# SAT and VAL denotes the s and v value in hsv color space
LEVEL_NOT_REQUIRED = -1
SAT_LEVEL_LOW = 0
SAT_LEVEL_MED = 1
SAT_LEVEL_HIGH = 2
VAL_LEVEL_LOW = 0
VAL_LEVEL_MED = 1
VAL_LEVEL_HIGH = 2


def level_check_factory(thresholds):
    def inner(level, data):
        if level == LEVEL_NOT_REQUIRED:
            return True
        if not (0 <= level < len(thresholds)-1):
            raise ValueError, "Unknown level %r" % level

        low, up = thresholds[level:level+2]
        return low < data <= up
    return inner

sat_level_check = level_check_factory([0, 0.4, 0.8, 1])
val_level_check = level_check_factory([0, 0.4, 0.8, 1])
