# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 13:07:33
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-12 11:23:38
from __future__ import division, print_function

import os
import traceback
from itertools import product

try:
    import cPickle as pickle
except ImportError:
    import pickle

import numpy as np
import cv2


from website.config import DATASET_DIR
from website.core.config import IMAGE_INDEX_TTH_FILE, IMAGE_INDEX_TTH_DATA_FILE
from website.core.algorithm import LSH, MMCQ
from website.core.algorithm.utility import get_theme_colors, hsv_reduce_colors, rgb_to_hsv
from website.utility import full_path_dataset


def vectorize(im):
    """assert im in float type and in RGB mode"""

    # theme_colors, theme_weights, s, v = get_theme_colors('', im=im)
    # theme_colors is a int type 2d np.array with max value 255
    # while theme_weights is a 1d float array

    dps = []

    block_w, block_h = im.shape[0] // 2, im.shape[1] // 2

    for i, j in product(range(2), range(2)):
        region = im[i*block_w:(i+1)*block_w, i*block_h:(i+1)*block_h]
        colors = MMCQ(region, 8, 2)
        colors, weights = zip(*colors)
        # hsv_colors = rgb_to_hsv(colors) / 255

        # h, s, v = np.split(hsv_colors, 3, axis=1)
        # x, y, z = s * v * np.cos(h), s * v * np.sin(h), v
        # hsv_colors = np.hstack([x, y, z])

        # weights = np.array(weights)

        # dps = np.hstack([hsv_colors, weights.reshape(-1, 1)])
        dps.append(np.hstack(colors))

    return np.hstack(dps)


def create_index():
    lsh = LSH(d=24, l=16)
    data = []

    try:
        for filename in os.listdir(DATASET_DIR):
            if not filename.endswith('.jpg'):
                continue

            print("Processing '%s'..." % filename)
            im = cv2.imread(full_path_dataset(filename))
            im = im[:, :, ::-1].astype(np.double)  # BGR -> RGB

            dps = vectorize(im)

            data.append(dps)
            lsh.feed(dps)

    except Exception, e:
        traceback.print_exc()
    else:
        print("Images indexing ends.")
    finally:
        lsh.compress()
        lsh.save(IMAGE_INDEX_TTH_FILE)

        with open(IMAGE_INDEX_TTH_DATA_FILE, 'wb') as f:
            pickle.dump(np.array(data), f)

        print("Image index saved to %s" % IMAGE_INDEX_TTH_FILE)


def get_search_func():
    lsh = LSH.restore(IMAGE_INDEX_TTH_FILE)

    with open(IMAGE_INDEX_TTH_DATA_FILE, 'rb') as f:
        data = pickle.load(f)

    print("TTH index data loaded")

    def search(im, max_n=50):
        im = im[:, :, ::-1]
        dp = vectorize(im)

        inds = lsh.find_neighbor(dp)

        dist = np.linalg.norm(data[inds] - dp, axis=1) / 30.0  # todo: hard code

        # get max_n-th cloest
        max_n = min(len(inds)-1, max_n)
        ret = np.argpartition(dist, max_n)[:max_n]
        ret = ret[np.argsort(dist[ret])]

        inds = np.array(inds)[ret]

        print("TTH: Match inds(begin with 0):\t", inds)
        print("TTH: Vector distance:\t", dist[ret])

        score = 1 / (dist[ret]+1)

        return inds, score

    return search
