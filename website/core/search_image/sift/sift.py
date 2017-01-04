# -*- coding:utf-8 -*-
# Created by GigaFlower at 16/11/30
# Implementing SIFT algorthim with python and opencv
#
# Paper:
# https://www.robots.ox.ac.uk/~vgg/research/affine/det_eval_files/lowe_ijcv2004.pdf

from __future__ import division, print_function

from itertools import product

import cv2
import numpy as np

from util import *
from config import *
from pyramid import Pyramid
from keypoint import CV2KeypointFinder, DoGKeypointFinder
from descriptor import DescriptorCalculator, DescriptorMatcher


class SIFT:
    def __init__(self, debug=True):
        self.pyramid = Pyramid()
        self.debug = debug

    #########################
    # Interfaces
    #########################
    def match(self, im1, im2, draw_matches=True, match_filename="matches.jpg",
              use_cv2_keypoints=True, use_bilinear_interp=False,
              draw_keypoints=False, kp_filename1="kp1.jpg", kp_filename2="kp2.jpg",
              descriptors1=None, positions1=None, descriptors2=None, positions2=None
              ):
        if descriptors1 is not None and positions1 is not None:
            dp1, pos1 = descriptors1, positions1
        elif im1 is None:
            raise ValueError, "Empty image 'im1' is given!"
        else:
            self._log("processing img1...")
            dp1, pos1 = self.process(im1, draw_keypoints=draw_keypoints, kp_filename=kp_filename1)

        if descriptors2 is not None and positions2 is not None:
            dp2, pos2 = descriptors2, positions2
        elif im2 is None:
            raise ValueError, "Empty image 'im2' is given!"
        else:
            self._log("\nprocessing img2...")
            dp2, pos2 = self.process(im2, draw_keypoints=draw_keypoints, kp_filename=kp_filename2)

        self._log("\nmatching...")
        dp_matcher = DescriptorMatcher()
        matches, cnt = dp_matcher(dp1, dp2)
        matches = sorted(matches, key=lambda x: x[2])

        self._log("During %d descriptors matching %d," % (dp1.shape[0], dp2.shape[0]))
        self._log("%d succeed\n%d failed with multiple peaks\n%d failed with too large the distance" % tuple(cnt))
        self._log("Matching done.")

        self._log("")
        if draw_matches:
            self.draw_matches(im1, pos1, im2, pos2, matches, filename=match_filename)

        self._log("\nFinished.")

        return self.match_for_human(matches, pos1, pos2)

    def process(self, im, save_pyramid=False, draw_keypoints=True, kp_filename="keypoints.jpg",
                use_cv2_keypoints=True, use_bilinear_interp=False):

        if im is None:
            raise ValueError, "Empty image is given!"

        if len(im.shape) != 2:
            raise ValueError, "Only gray scale image is acceptable"

        if use_cv2_keypoints:
            kp_finder = CV2KeypointFinder()
        else:
            kp_finder = DoGKeypointFinder()

        dp_calculator = DescriptorCalculator()

        self.pyramid.construct(im)
        self.pyramid.compute_grad()

        # get raw keypoints

        self._log("detecting keypoints...")
        n1, n2 = self.pyramid.find_keypoints(kp_finder, n_max_per_layer=para.max_keypoints_per_layer)
        self._log("%d keypoints found, and %d accounting orientations." % (n1, n2))

        self._log("computing descriptors...")
        descriptors, pos = dp_calculator(self.pyramid, use_bilinear_interp)

        self._log("%d x %d descriptors calculation done." % descriptors.shape)

        # save result if need
        if save_pyramid:
            for i, j, im in self.pyramid.enumerate():
                cv2.imwrite("pyramid/pyramid_octave_{}_img_{}.jpg".format(i, j), im)

        if draw_keypoints:
            kps = self.pyramid.flattened_keypoints
            self.draw_keypoints(im, kps, filename=kp_filename)

        return descriptors, pos

    ##########################
    # Result visualization
    ##########################
    def draw_keypoints(self, im, keypoints, filename="keypoints.jpg"):
        self._log("drawing keypoints into '%s'..." % filename)
        rows, cols = im.shape

        def to_cv2_kp(kp):
            # assert kp = [<row>, <col>, <ori>, <octave_ind>, <layer_ind>]
            ratio = get_size_ratio_by_octave(kp[3])
            scale = get_scale_by_ind(kp[3], kp[4])
            return cv2.KeyPoint(kp[1] / ratio, kp[0] / ratio, 10, kp[2] / PI * 180)

        kp_for_draw = list(map(to_cv2_kp, keypoints))
        im_kp = cv2.drawKeypoints(im, kp_for_draw, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imwrite(filename, im_kp)

    def draw_matches(self, im1, pos1, im2, pos2, matches, filename="matches.jpg"):
        self._log("drawing matches into '%s'..." % filename)
        row1, col1 = im1.shape
        row2, col2 = im2.shape

        im_out = np.zeros((max(row1, row2), col1+col2, 3), dtype=np.uint8)
        im_out[:row1, :col1] = np.dstack([im1]*3)
        im_out[:row2, col1:] = np.dstack([im2]*3)

        l = len(matches)

        for ind, (i, j, d) in list(enumerate(matches))[::-1]:
            d /= para.descr_match_threshold  # map to [0, 1]
            _pos1, _pos2 = pos1[i], pos2[j]
            color = hsv_to_rgb(int(d * 120 - 120), 1, 1 - d / 3)
            color = [int(c * 255) for c in color]
            cv2.line(im_out, (_pos1[1], _pos1[0]), (_pos2[1]+col1, _pos2[0]), color, 1)

        cv2.imwrite(filename, im_out)

    ##########################
    # Utility
    ##########################
    @staticmethod
    def match_for_human(matches, pos1, pos2):
        return [(list(pos1[i]), list(pos2[j]), v) for i, j, v in matches]

    def _log(self, info):
        if self.debug:
            print(info)


def cv2_match(im1, im2):
    mysift = SIFT()
    sift = cv2.SIFT()
    bf = cv2.BFMatcher()


    kp1, dp1 = sift.detectAndCompute(im1, None)
    kp2, dp2 = sift.detectAndCompute(im2, None)
    matches_ = bf.knnMatch(dp1, dp2, k=2)

    print(len(matches_))
    good = []
    for m, n in matches_:
        if m.distance < 0.90 * n.distance:
            good.append(m)
    print(len(good))

    pos1 = [(int(kp.pt[1]), int(kp.pt[0])) for kp in kp1]
    pos2 = [(int(kp.pt[1]), int(kp.pt[0])) for kp in kp2]
    matches = [(m.queryIdx, m.trainIdx, 0.15) for m in good]

    cv2.imwrite("cvkp1.jpg", cv2.drawKeypoints(im, kp1, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))
    cv2.imwrite("cvkp2.jpg", cv2.drawKeypoints(imm, kp2, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS))
    mysift.draw_matches(im, pos1, imm, pos2, matches, 'ckmatch.jpg')

if __name__ == '__main__':

    sift = SIFT()
    im = cv2.imread('target.jpg', 0)
    imm = cv2.imread('dataset/01.jpg', 0)
    # sift.match(im, imm ,match_filename="a3.jpg",draw_keypoints=True,kp_filename1="a1.jpg",kp_filename2="a2.jpg")
    cv2_match(im, imm)
