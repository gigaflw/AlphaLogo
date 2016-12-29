# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-28 22:46:45
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-29 21:15:32

from __future__ import division, print_function

import os
import numpy as np
import cv2


def hist(im):
    h = cv2.calcHist([im], [0], None, [256], [0, 256]).reshape((-1))
    return h


def norm(vec):
    return np.sqrt(np.sum(vec**2))


class VBox(object):
    hist = []

    @classmethod
    def init_hist(cls, im):
        hist = np.zeros((256,256,256))
        
        for b,g,r in im.reshape((-1, 3)):
            hist[b,g,r] += 1

        cls.hist = hist


    def __init__(self, r1=0, r2=256, g1=0, g2=256, b1=0, b2=256):
        self.bounds = [r1, r2, g1, g2, b1, b2]
        self.region = self.hist[slice(r1, r2), slice(g1, g2), slice(b1, b2)]

        sr, sg, sb = r2 - r1, g2 - g1, b2 - b1

        if sr >= sg and sr >= sb:
            self.max_span_color = 0
        elif sg >= sb:
            self.max_span_color = 1
        else:
            self.max_span_color = 2

    def split(self):
        axis = self.max_span_color
        c1, c2 = self.bounds[axis*2:axis*2+2]
        sum_axis = tuple(x for x in range(3) if x != axis)
        
        if c1 >= c2 - 1:
            return ()  # comma is necessary
        
        median = (self.region.sum(axis=sum_axis) * range(c1, c2)).sum() / self.region.sum()
        median = int(round(median))

        p1 = self.bounds
        p2 = p1[:]
        p1[axis * 2] = median
        p2[axis * 2 + 1] = median

        return filter(lambda b:b.region.sum()>0, (VBox(*p1), VBox(*p2)))

    def aver(self):
        for axis, c1, c2 in zip(range(3), self.bounds[::2], self.bounds[1::2]):
            sum_axis = tuple(x for x in range(3) if x != axis)
            aver = (self.region.sum(axis=sum_axis) * range(c1, c2)).sum() / self.region.sum()
            yield aver


def MMCQ(im):
    VBox.init_hist(im)
    boxes = [VBox()]
    tmp = []

    while len(boxes) < 8:
        for vbox in boxes:
            tmp.extend(vbox.split())
        boxes, tmp = tmp, []
    return [list(vbox.aver()) for vbox in boxes]


def main():
    for f in os.listdir('dataset'):
        if not f.endswith('14.jpg'):
            continue

        im = cv2.imread('dataset/%s' % f)
        colors = MMCQ(im)
        rows, cols, _ = im.shape

        n = np.zeros((rows, cols+20, 3), dtype=np.uint8) + 255
        n[:rows, :cols, :] = im

        for i,c in enumerate(colors):
            n[i*20: (i+1)*20, cols:cols+20, :] = [int(cc) for cc in c]

        cv2.imshow("test", n)
        cv2.waitKey(0)


if __name__ == '__main__':
    main()
