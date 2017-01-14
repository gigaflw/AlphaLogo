# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-28 22:46:45
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-13 16:49:53
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
# * split basis
#       Instead of `number_pixels * volume_of_color_cube` from the paper
#       a number based on relative variance is used, which gives a seemingly better result and
#       is more reasonable intuitively.
#
# TODO: more tests and statistics to prove the betterment
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
    def init(cls, im, color_level):
        """
        @param: im:
            the image array (type = np.ndarray), should have 3 channels

        @param: color_level:
            each color component (R,G,B) will be split into `color_level` levels
        """
        assert len(im.shape) == 3, "Only image with 3 color channels is accepeted"

        cls.color_level = color_level

        n = color_level
        ratio = 256 / n
        size = (n, n, n)

        im = (im / ratio).astype(np.int)
        indexes = list(im.reshape((-1, 3)).T)
        # `list` is necessary to be the right indexes

        color_cube = np.zeros((n, n, n), dtype=np.int)
        np.add.at(color_cube, indexes, 1)
        # add.at is used so that repeated color will be add repeatedly

        cls.im = im
        cls.color_cube = color_cube

    @classmethod
    def revert_color(cls, colors):
        """
        Since when spliting, a suppressed color level system (less than 256) is used,
        the result of MMCQ may be not in a 256-level color system.
        This function helps to revert them back to 256 level colors.

        @param: colors: a iterable of numbers
        @returns: a iterable of numbers, int type
        """
        # 0.5 is to map the color to the center of the range
        return [int((c+0.5) / cls.color_level * 256) for c in colors]

    def __init__(self, r1=0, r2=None, g1=0, g2=None, b1=0, b2=None):
        if r2 is None or g2 is None or b2 is None:
            r2 = g2 = b2 = self.color_level

        cube = self.color_cube[r1:r2, g1:g2, b1:b2]

        self.n_pix = int(cube.sum())
        self.n_pix_partial = [cube.sum(axis=axis) for axis in [(1, 2), (0, 2), (0, 1)]]
        # n_pix_partial[0] is the list of n_pix along aixs R, also have 1 -> G, 2 -> B

        self.bounds = [(r1, r2), (g1, g2), (b1, b2)]
        self.unsplitable = False

        if self.is_empty:
            aver, var = [0, 0, 0], [0, 0, 0]
        else:
            aver, var = zip(*self.aver_and_var())

        self.aver, self.var = aver, var
        self._color_var_rel = [var[i] / (self.bounds[i][1] - self.bounds[i][0]) for i in range(3)]

    def split(self):
        """
        Split the vbox into 2 vboxes with same n_pixels
        If the box is empty, an error will happen.
        """
        assert not self.is_empty, "Can't split an empty box"

        axis = self.widest_color
        c1, c2 = self.bounds[axis]

        if c2 - c1 <= 1:
            # can't split

            if not self.unsplitable:
                self.unsplitable = True  # this will make its priority order the lowest
                return (self, )  # do not split
            else:
                return (self, self)  # meet again, which means no other splitable cubes

        else:
            median = np.average(range(c1, c2), weights=self.n_pix_partial[axis])
            median = int(round(median))
            median = min(c2-1, max(c1+1, median))

            p1 = sum(map(list, self.bounds), [])  # [(r1, r2), (g1, g2), (b1, b2)] -> [r1,r2,g1,g2,b1,b2]
            p2 = p1[:]
            p1[axis * 2] = median
            p2[axis * 2 + 1] = median
            # print("Split result:", p1, p2)
            return filter(lambda b: not b.is_empty, (VBox(*p1), VBox(*p2)))

    def aver_and_var(self):
        """
        The average and variance along 3 color axis in the vbox

        In total, 6 floats will be yields

        @yield: aver_color, var_of_color
            all floats
        """
        # assert not self.is_empty

        for axis in range(3):
            c1, c2 = self.bounds[axis]
            w = self.n_pix_partial[axis]
            aver = np.average(np.arange(c1, c2), weights=w)
            var = np.average(np.arange(c1, c2)**2, weights=w) - aver ** 2  # D = E(X^2) - (EX)^2
            yield aver, var

    @property
    def is_empty(self):
        return self.n_pix == 0

    @property
    def widest_color(self):
        return max(enumerate(self._color_var_rel), key=lambda x: x[1])[0]

    @property
    def split_necessity(self):
        """
        A number denoting how necessary the color cube should be split.
        The larger, the more necessary.

        Considering 
            1) the spread of colors
            2) number of pixels
        """
        return max(self._color_var_rel) * self.n_pix
        # return reduce(int.__mul__, (l-u for u,l in self.bounds)) * self.n_pix

    def __lt__(self, other):
        """
        Necessary to enable priority queue sorting
        The smaller (returns `True`), the higher priority, the more likely to be split
        """
        return not (self.unsplitable or self.split_necessity < other.split_necessity)


def MMCQ(im, color_level, slots):
    """
    A implementation of MMCQ (modified median cut quantification) algorithm

    @param: im:
        the image array (type = np.ndarray), should have 3 channels.
        The order and the type of channels are not specified,
         the returned colors will be in the same type of channels,
        i.e. given a RGB image, return RGB colors, and HSV colors for HSV images, etc.

    @param: color_level:
        each color component (R,G,B) will be split into `color_level` levels

    @param: slots:
        number of returned colors

    @return: a list like 
        [([r,g,b], pixel weights), (..,), ...]
        the pixel weights not necessarily add up to 1 !
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

    return [(VBox.revert_color(box.aver), box.n_pix/box.im.size)
            for box in sorted(ret, key=lambda x:x.n_pix, reverse=True)]


def demo():
    import cv2

    path = "../../static/dataset"

    for f in os.listdir(path):
        if not f.endswith('.jpg'):
            continue

        im = cv2.imread(os.path.join(path, f))
        colors = MMCQ(im, color_level=8, slots=8)
        colors, weights = zip(*colors)

        rows, cols, _ = im.shape

        n = np.zeros((rows, cols+200, 3), dtype=np.uint8) + 255
        n[:rows, :cols, :] = im

        cv2.rectangle(n, (cols+9, 29), (cols+190, 190), (0, 0, 0))
        for i, c in enumerate(colors):
            n[i*20+30: (i+1)*20+30, cols+10:cols+190, :] = [int(cc) for cc in c]

        cv2.imshow("test", n)

        cv2.waitKey(0)


if __name__ == '__main__':
    demo()
