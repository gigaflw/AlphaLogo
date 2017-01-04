# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 13:07:33
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-04 16:35:08


try:
    import cPickle as pickle
except ImportError:
    import pickle

import numpy as np
import cv2
import os

from website.config import DATASET_DIR
from website.core.config import IMAGE_INDEX_PKL_FILE
from website.core.search_image.sift import SIFT
from website.core.search_image.lsh import LSH


def create_index():
    sift = SIFT(debug=False)
    lsh = LSH(d=128, l=6)
    n = 0
    for fname in os.listdir(DATASET_DIR):
        if not fname.endswith('.jpg'):
            continue

        im_path = os.path.join(DATASET_DIR, fname)
        print("Processing '%s'..." % im_path)
        dps, _ = sift.process(cv2.imread(im_path, 0))
        lsh.feed_n(dps)
        n+=1
        if n>100:
            break
    lsh.save(IMAGE_INDEX_PKL_FILE)
    print("Images indexing ends.")


def get_search_func():
    sift = SIFT(debug=False)
    lsh = LSH.restore(IMAGE_INDEX_PKL_FILE)
    print("Image index data loaded")

    def search(im, max_n=10):
        dps, _ = sift.process(im)
        return lsh.match(dps, max_n=max_n)

    return search
