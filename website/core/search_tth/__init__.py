# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 13:07:33
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-11 14:24:21

import os
import traceback

import numpy as np
import cv2

from website.config import DATASET_DIR
from website.core.config import IMAGE_INDEX_TTH_FILE
from website.core.algorithm import LSH, MMCQ
from website.core.algorithm.utility import get_theme_colors, hsv_reduce_colors
from website.utility import full_path_dataset


def vectorize(im):
    im = im[:, :, ::-1]  # BGR -> RGB

    colors = MMCQ(im, color_level=8, slots=8)

    colors, weights = zip(*colors)
    colors = np.array(colors)

    theme_colors, theme_weights = hsv_reduce_colors(colors, weights, 0.1, return_rgb=False)

    # theme_colors, theme_weights, s, v = get_theme_colors('', im=im)
    # theme_colors is a int type 2d np.array with max value 255
    # while theme_weights is a 1d float array

    dps = np.hstack([theme_colors, theme_weights.reshape(-1,1)])
    return dps


def create_index():
    lsh = LSH(d=4, l=32)

    try:
        for filename in os.listdir(DATASET_DIR):
            if not filename.endswith('.jpg'):
                continue

            print("Processing '%s'..." % filename)
            im = cv2.imread(full_path_dataset(filename))
            dps = vectorize(im)

            lsh.feed_n(dps)

    except Exception, e:
        traceback.print_exc()
        raise
    else:
        print("Images indexing ends.")
    finally:
        lsh.compress()
        lsh.save(IMAGE_INDEX_TTH_FILE)
        print("Image index saved to %s" % IMAGE_INDEX_TTH_FILE)


def get_search_func():
    lsh = LSH.restore(IMAGE_INDEX_TTH_FILE)
    print("TTH index data loaded")

    def search(im, max_n=10):
        dps = vectorize(im)

        return lsh.match(dps, max_n=max_n)

    return search
