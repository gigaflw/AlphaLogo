# -*- coding: utf-8 -*-
# @Author: BigFlower
# @Date:   2016-12-23 16:54:28
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-04 12:55:11

from __future__ import division, print_function
import numpy as np
import cv2

try:
    import cPickle as pickle
except ImportError:
    import pickle

import bisect

from sift import SIFT


class LSH:

    """
    usage:

    l = LSH()
    for dp in descriptors
    l.feed(dp)
    """

    def __init__(self, d, l=4):
        """
        @param: d : dimension of the descriptor
        @param: l : number of hash functions
        """
        self.d = d
        self.l = l

        self._hash_tables = {}
        # self._descriptors = []

        self._rand_vec = np.random.random((l, d)) * 2 - 1
        self._dp_ind = 0
        self._im_ind = 0
        self._im_dps = []
        self._im_dps_cum = [0]

    def feed(self, dp):
        self.lsh_hash_and_save(dp)
        # self._descriptors.append(dp)

    def feed_n(self, dps):
        for dp in dps:
            self.lsh_hash_and_save(dp)
        self._im_ind += 1

        self._im_dps.append(len(dps))
        self._im_dps_cum.append(len(dps) + self._im_dps_cum[-1])
        # self._descriptors.extend(dps)

    def clear(self):
        # self._descriptors = []
        self._dp_ind = 0
        self._im_ind = 0
        self._hash_tables = {}
        self._im_dps = []
        self._im_dps_cum = [0]

    # def randomize_index(self):
    #     self._rand_vec = [np.random.random((1, self.d)) * 2 - 1 for _ in range(self.l)]
    #     self.rebuild()

    # def rebuild(self):
    #     self._dp_ind = 0
    #     self._hash_tables = [{} for _ in range(self.l)]

    #     for dp in self._descriptors:
    #         self.lsh_hash_and_save(dp)

    def match(self, dps, max_n=30):
        stat = np.zeros(self._im_ind)
        max_n = min(self._im_ind, max_n)

        for dp in dps:
            im_inds = self.lsh_match(dp)
            stat[im_inds] += 1

        ret = np.argpartition(stat, -max_n)[-max_n:]
        ret = ret[np.argsort(stat[ret])][::-1]
        print(stat[ret])

        return ret

    def lsh_match(self, dp):
        cosine_hash = self.lsh_hash(dp)
        bucket = self._hash_tables.get(cosine_hash, ())
        ret = bucket

        # return list(map(self.dp_ind_to_im_ind, ret))
        return ret

    def dp_ind_to_im_ind(self, dp_ind):
        return bisect.bisect(self._im_dps, dp_ind) - 1

    def lsh_hash(self, dp):
        return self.cosine_hash(dp, self._rand_vec)

    def lsh_hash_and_save(self, dp):
        cosine_hash = self.cosine_hash(dp, self._rand_vec)
        self._hash_tables.setdefault(cosine_hash, []).append(self._im_ind)
        self._dp_ind += 1

    @staticmethod
    def cosine_hash(vec, rand_vecs):
        """
        e.g.
        >>> cosine_hash([1.0, 1.5, 2.1, 0.3, 0.7, 0.6], [1, -1, -1, 1, -1, 1])
        0

        the process is:
        return the sign of dot product
        -> return int(v1 * v2 > 0)
        """
        # theta = np.arccos(np.dot(vec, rand_vec)) / (np.pi/2)# [0, 1]
        # ret = int(theta * 20)
        ret = (np.dot(vec, rand_vecs.T) > 0).astype(np.int)
        return tuple(ret)

    def save(self, filename='lsh.pickle'):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def restore(filename='lsh.pickle'):
        with open(filename, 'rb') as f:
            return pickle.load(f)

def l_check(dpss):
    for l in range(6, 17, 2):
        lsh = LSH(d=128, l=l)

        # for i in range(100):
            # dps, _ = sift.process(cv2.imread("../../index/images/%05d.jpg" % (i+1), 0))
        for dps in dpss:
            lsh.feed_n(dps)
        lsh.save("lsh-%d.pickle" % l)

        dps, _ = sift.process(cv2.imread("../../index/images/test.jpg", 0))
        t1 = time.time()
        print(lsh.match(dps, max_n=10) + 1, end='\t')
        print(time.time() - t1)


if __name__ == '__main__':
    import time
    import cProfile as profile

    sift = SIFT()

    lsh = LSH(d=128, l=6)

    # for j in range(4):
    #     for i in range(j*100, (j+1)*100):
    #         dps, _ = sift.process(cv2.imread("../../index/images/%05d.jpg" % (i+1), 0))
    #         lsh.feed_n(dps)
    #     lsh.save("lsh-n-%d.pickle" % j)

    lsh = LSH.restore('lsh-n-0.pickle')
    dps, _ = sift.process(cv2.imread("../../index/images/test.jpg", 0))
    t1 = time.time()
    print(lsh.match(dps, max_n=10) + 1, end='\t')
    print(time.time() - t1)

    # profile.run("lsh.match(dps)","a.profile")
    # # t0 = time.time()
    # # t = time.time() - t0
    # # print(t)
