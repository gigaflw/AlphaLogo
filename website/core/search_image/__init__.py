# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 13:07:33
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-13 15:45:38
# 
# Image search algorithm based on SIFT and LSH
# The implementation locates at 'website.core.algorirhm', here is the interface
# 
import os
import traceback

import numpy as np
import cv2

from website.config import DATASET_DIR
from website.core.config import IMAGE_INDEX_PKL_FILE
from website.core.algorithm import SIFT, LSH


def create_index():
    """
    For each jpg logo image in `DATASETDIR`, a vector will be computed.
    Then, create index file for sift search, whose data is compressed by LSH.
    Index file will be saved to `IMAGE_INDEX_PKL_FILE`
    """
    sift = SIFT(debug=False)
    lsh = LSH(d=128, l=12) # 128 = dimension of SIFT descriptor, 12 = experience number of hash function
    i = 0
    try:
        for fname in os.listdir(DATASET_DIR):
            if not fname.endswith('.jpg'):
                continue

            im_path = os.path.join(DATASET_DIR, fname)
            print("Processing '%s'..." % im_path)
            dps, _ = sift.process(cv2.imread(im_path, 0))
            lsh.feed_n(dps)

            i+= 1
            if i >= 100:
                break

    except Exception, e:
        traceback.print_exc()
    else:
        print("Images indexing ends.")
    finally:
        lsh.compress()
        lsh.save(IMAGE_INDEX_PKL_FILE)
        print("Image index saved to %s" % IMAGE_INDEX_PKL_FILE)


def get_search_func():
    """
    Lazy load search function by SIFT and LSH.
    @return: a search function
    @the search function's return:
        two list, the first is the list of indexes of images matched in the SIFT data index file,
        the second is the list of scores ranging in [0, 1], the larger the score, the better the match
    """
    sift = SIFT(debug=False)
    lsh = LSH.restore(IMAGE_INDEX_PKL_FILE)
    print("Image index data loaded")

    def search(im, max_n=20):
        if len(im.shape) == 3:
            im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        import time
        t0 = time.time()
        dps, _ = sift.process(im)
        t1 = time.time()
        ret = lsh.match(dps, max_n=max_n)
        t2 = time.time()
        print(t1 - t0)
        print(t2 - t1)
        return ret

    return search
