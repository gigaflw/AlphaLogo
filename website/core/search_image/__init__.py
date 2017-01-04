# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 13:07:33
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-04 12:58:59


try:
    import cPickle as pickle
except ImportError:
    import pickle

import numpy as np
import cv2
import os

from website.config import DATASET_DIR

from website.core.search_image.sift import SIFT
from website.core.search_image.lsh import LSH


def create_index():
    sift = SIFT(debug=False)
    lsh = LSH(d=128, l=6)

    for i in range(100):
        im_path = os.path.join(DATASET_DIR, '%05d.jpg' % (i+1))
        print("Processing '%s'..." % im_path)
        dps, _ = sift.process(cv2.imread(im_path), 0)
        lsh.feed_n(dps)
    lsh.save("lsh.pkl")


def get_search_func():
    sift = SIFT(debug=False)
    lsh = LSH.restore('lsh.pkl')
    print("LSH data loaded")

    def search(im, max_n=10):
        dps, _ = sift.process(im)
        return lsh.match(dps, max_n=max_n) 

    return search
