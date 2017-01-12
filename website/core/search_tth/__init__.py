# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 13:07:33
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-12 21:20:46
# 
# The vectorize, index and search algorithm based on color vectors
# No specific name, so the aurthor's name's abbreviation is used, i.e. 'tth'
# 
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


def vectorize(im, n=2, color_level=8):
    """
    @param: im: float type 3d array, in RGB color mode
    @param: n: the image will be split into `n*n` blocks and comput vector respectively
    @param: color_level: the precision of floats for each RGB component, no more than 256

    Compute the color vector of the image, two main RGB color will be extrieve in each block,
    thus a (n*n) * 6 -d vector will be returned. 
    The main color is conputed by MMCQ algorithm
    """

    dps = []

    block_w, block_h = im.shape[0] // n, im.shape[1] // n

    for i, j in product(range(n), range(n)):
        region = im[i*block_w:(i+1)*block_w, i*block_h:(i+1)*block_h]
        colors = MMCQ(region, color_level, 2)
        colors, weights = zip(*colors)

        dps.append(np.hstack(colors))

    return np.hstack(dps)


def create_index():
    """
    For each jpg logo image in `DATASETDIR`, a vector will be computed.
    An `LSH` instance will be fed the vector, both the LSH and vectors will be piclked.

    `LSH` will be saved into `IMAGE_INDEX_TTH_FILE`, and vectors into `IMAGE_INDEX_TTH_DATA_FILE`
    """
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
            pickle.dump(np.array(data), f, protocol=2)

        print("Image index saved to %s" % IMAGE_INDEX_TTH_FILE)


def get_search_func():
    """
    Lazy load search function factory

    @the search function's return:
    two list, the first is the list of indexes of images matched in the SIFT data index file,
    the second is the list of scores ranging in [0, 1], the larger the score, the better the match

    A image in RGB color mode is asserted as the argument.
    """
    lsh = LSH.restore(IMAGE_INDEX_TTH_FILE)

    with open(IMAGE_INDEX_TTH_DATA_FILE, 'rb') as f:
        data = pickle.load(f)

    print("TTH index data loaded")

    def search(im, max_n=50):
        dp = vectorize(im)

        inds = lsh.find_neighbor(dp)

        dist = np.linalg.norm(data[inds] - dp, axis=1) / 30.0  # todo: hard code, 30 is experience threshold

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
