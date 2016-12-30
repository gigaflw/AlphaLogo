# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-28 22:46:45
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-30 17:21:32
#
# MMCQ (Modified Median Cut Quantization) Algorithm
# src: http://collaboration.cmc.ec.gc.ca/science/rpn/biblio/ddj/Website/articles/DDJ/1994/9409/9409e/9409e.htm
# also reference: https://github.com/lokesh/color-thief
#
# Improvements:
# * splitable flag
#       Chances are that one vbox is not splitable, in this case, we mark this as unsplitable 
#   and returns itself when it is required to split.
#       This mark will give the vbox lowest priority, which ensures this will not be required to split
#   the second time unless all other boxes are unsplitable.
#       When the second require happens, it split into 2 same one, (i.e. two copy of itself), 
#    since it is unsplitable.
# 
# * ignore lonely pixels
#       If pixels with some kinds of color has too small a proportion (here, the threshold is 0.001),
#   we discard it instead of stubbornly requiring it to split , in order to give a more accurate result
# 


from __future__ import division, print_function

import os
try:
    from Queue import PriorityQueue
except ImportError:
    from queue import PriorityQueue  # py3

import numpy as np


class VBox(object):

    @classmethod
    def init(cls, im, color_level, weight_threshold=0.001):
        """
        @param: im:
            the image array (type = np.ndarray), should have 3 channels

        @param: color_level:
            each color component (R,G,B) will be split into `color_level` levels

        @param: weight_threshold:
            box with pixel proportion lower than this will be ignored.
            This should be small enough accounting to the image.
            By default it is 0.001
        """
        assert len(im.shape) == 3, "Only image with 3 color channels is accepeted"

        cls.color_level = color_level
        cls.n_pix_threshold = weight_threshold * (im.shape[0] * im.shape[1])

        n = color_level
        ratio = 256 / n
        size = (n, n, n)

        indexes = list((im.reshape((-1, 3)).T / ratio).astype(np.int))
        # list is necessary to get the right indexes

        color_cube = np.zeros((n, n, n), dtype=np.int)
        np.add.at(color_cube, indexes, 1)
        # add.at is used so that repeated color will be add repeatedly

        cls.color_cube = color_cube

    @classmethod
    def convert_color_level(cls, colors):
        # 0.5 is to map the color to the center of the range
        return [int((c+0.5) / cls.color_level * 256) for c in colors]

    def __init__(self, r1=0, r2=None, g1=0, g2=None, b1=0, b2=None):
        if r2 is None or g2 is None or b2 is None:
            r2 = g2 = b2 = self.color_level

        region = self.color_cube[r1:r2, g1:g2, b1:b2]
        # n_pix_partial[0] is the list of n_pix along aixs R, also 1 -> G, 2 -> B
        n_pix_partial = [region.sum(axis=axis) for axis in [(1, 2), (0, 2), (0, 1)]]

        # total pixels
        self.n_pix = region.sum()
        self.volume = (r2-r1) * (g2-g1) * (b2-b1)

        # get the color with widest span
        sr, sg, sb = r2 - r1, g2 - g1, b2 - b1
        widest_color = 0 if (sr >= sg and sr >= sb) else (1 if sg >= sb else 2)

        self.unsplitable = False

        # function define
        # use nested scope to avoid tedious property assignments
        def split():
            """
            Split the vbox into 2 vboxes with same n_pixels
            If the box is empty, nothing will be returned
            """
            assert not self.is_empty, "Some error happens"

            c1, c2 = [(r1, r2), (g1, g2), (b1, b2)][widest_color]

            if c2 - c1 <= 1:
                # can't split

                if self.unsplitable:
                    return (self, self)  # meet again, which means no other splitable cubes
                else:
                    self.unsplitable = True  # this will make its priority order the lowest
                    return (self, )  # do not split
            else:
                median = np.average(range(c1, c2), weights=n_pix_partial[widest_color])
                median = int(round(median))
                median = min(c2-1, max(c1+1, median))

                p1 = [r1, r2, g1, g2, b1, b2]
                p2 = p1[:]
                p1[widest_color * 2] = median
                p2[widest_color * 2 + 1] = median
                # print(round(self.volume / (self.color_level**3), 3), self.n_pix ,[r1,r2,g1,g2,b1,b2], p1, p2)
                return filter(lambda b: not b.is_empty, (VBox(*p1), VBox(*p2)))

        def aver():
            """
            The aver color in the vbox
            """
            assert not self.is_empty, "Some error happens"

            ret = []
            for axis in range(3):
                c1, c2 = [(r1, r2), (g1, g2), (b1, b2)][axis]
                aver = np.average(range(c1, c2), weights=n_pix_partial[axis])
                ret.append(aver)
            # print(round(self.volume / (self.color_level**3), 3), self.n_pix , [int(r) for r in ret])
            ret = self.convert_color_level(ret)
            return ret

        self.split = split
        self.aver = aver

    @property
    def is_empty(self):
        return self.n_pix == 0

    @property
    def almost_empty(self):
        return self.n_pix <= self.n_pix_threshold

    def __lt__(self, other):
        """
        Necessary to enable priority queue sorting
        The smaller (returns `True`), the higher priority, the more likely to be split
        """
        return not (self.unsplitable or self.n_pix * self.volume < other.n_pix * other.volume)


def MMCQ(im, color_level, slots):
    """
    A implementation of MMCQ (modified median cut quantification) algorithm

    @param: im:
        the image array (type = np.ndarray), should have 3 channels

    @param: color_level:
        each color component (R,G,B) will be split into `color_level` levels

    @param: slots:
        number of returned colors
    """
    # init
    VBox.init(im, color_level)
    q = PriorityQueue()
    q.put(VBox())

    # recursively split
    while q.qsize() < slots:
        box = q.get(timeout=0)
        for b in box.split():
            q.put(b)

    # format result
    ret = []
    while not q.empty():
        box = q.get(timeout=0)
        ret.append(box)

    return [box.aver() for box in sorted(ret, key=lambda x:x.n_pix, reverse=True)]


def demo():
    import cv2

    for f in os.listdir('../static/dataset'):
        if not f.endswith('.jpg'):
            continue

        im = cv2.imread('../static/dataset/%s' % f)
        colors = list(MMCQ(im, color_level=256, slots=16))
        rows, cols, _ = im.shape

        n = np.zeros((rows, cols+20, 3), dtype=np.uint8) + 255
        n[:rows, :cols, :] = im

        for i, c in enumerate(colors):
            n[i*10: (i+1)*10, cols:cols+20, :] = [int(cc) for cc in c]

        cv2.imshow("test", n)
        cv2.waitKey(0)


if __name__ == '__main__':
    demo()
