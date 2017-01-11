# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 13:07:33
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-11 10:49:44

import os
import traceback

import numpy as np
import cv2

from website.config import DATASET_DIR
from website.core.config import IMAGE_INDEX_PKL_FILE
from website.core.algorithm import SIFT, LSH


def create_index():
    sift = SIFT(debug=False)
    lsh = LSH(d=128, l=12)

    try:
        for fname in os.listdir(DATASET_DIR):
            if not fname.endswith('.jpg'):
                continue

            im_path = os.path.join(DATASET_DIR, fname)
            print("Processing '%s'..." % im_path)
            dps, _ = sift.process(cv2.imread(im_path, 0))
            lsh.feed_n(dps)

    except Exception, e:
        traceback.print_exc()
    else:
        print("Images indexing ends.")
    finally:
        lsh.compress()
        lsh.save(IMAGE_INDEX_PKL_FILE)
        print("Image index saved to %s" % IMAGE_INDEX_PKL_FILE)


def get_search_func():
    sift = SIFT(debug=False)
    lsh = LSH.restore(IMAGE_INDEX_PKL_FILE)
    print("Image index data loaded")

    def search(im, max_n=10):
        if len(im.shape) == 3:
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        dps, _ = sift.process(im)
        return lsh.match(dps, max_n=max_n)

    return search
