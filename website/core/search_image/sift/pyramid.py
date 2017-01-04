# -*- coding:utf-8 -*-
# Created by GigaFlower at 16/12/16

from itertools import product

import numpy as np
import cv2

from util import *
from config import *

cv2_gaussian = cv2.GaussianBlur
cv2_gaussian_kernel = cv2.getGaussianKernel


class Pyramid:

    """
    Construct a image pyramid P, where
        P[i] = <i-th octave>
        P[i][j] = <j-th image in i-th octave>

        len(P[i]) = s+3
        P[i][?].size = 1/4 * P[i-1][?].size (i.e. half in side length)

        Let σ_i,j denote the scale of P[i][j] in math, then
            σ_i,j =  kσ_i,j-1
            σ_i,0 = σ_i-1,<last_one_but_one> = σ_i-1,s+1
                = 2 * σ_i-1,0
            σ_0,0 is set by experience

        Let s_i,j denote the sigma used to Guassian blur the image, then
            s_i,j = k * s_i,j-1
            s_i,0 = s_0,0 = σ_0,0
    """

    def __init__(self):
        self._pyramid = []

        self._grad_mag = []
        self._grad_ang = []
        self._keypoints = []

    @property
    def n_octaves(self):
        return len(self._pyramid)

    @property
    def n_layers_per_octave(self):
        if self._pyramid:
            return len(self._pyramid[0])
        else:
            return None

    @property
    def keypoints(self):
        return self._keypoints
    
    @property
    def flattened_keypoints(self):
        """
        flatten后，下标信息octave_ind 和 layer_ind丢失，需要添上
        """
        for octave_ind, layer_ind, kps in self.enumerate(self._keypoints):
            for kp in kps:
                yield kp + [octave_ind, layer_ind]

    @property
    def n_keypoints(self):
        n = 0
        for _, __, kps in self.enumerate(self._keypoints):
            n += len(kps)
        return n

    def _flatten(self):
        if not lst or not isinstance(lst[0], list):
            return lst
        else:
            return sum([self._flatten(x) for x in lst], [])

    def construct(self, im):
        pyramid = self._pyramid = []

        # todo: size
        while im.size > para.pyramid_top_size:
            im_ = im.copy()
            pyramid.append([])

            for layer_ind in range(para.pyramid_octave_layers):
                im_ = cv2_gaussian(im_, para.gaussian_size, get_sigma_by_layer(layer_ind))
                pyramid[-1].append(im_)

            im = cv2.resize(im, (0, 0), fx=para.pyramid_size_ratio, fy=para.pyramid_size_ratio)

        l1, l2 = self.n_octaves, self.n_layers_per_octave
        for name in ['_grad_mag', '_grad_ang', '_keypoints']:
            setattr(self, name, [[None] * l2 for _ in range(l1)])

    def compute_grad(self):
        """
        precompute gradient's magnitude and angle of pyramid
            where angle is between (0, 2π)
        """

        for oct_ind, layer_ind, layer in self.enumerate():
            # todo: better kernel can be used?
            grad_x = cv2.filter2D(layer, cv2.CV_64F, np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]))
            grad_y = cv2.filter2D(layer, cv2.CV_64F, np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]))
            grad_mag = np.sqrt(grad_x**2 + grad_y**2)
            grad_ang = np.arctan2(grad_y, grad_x)  # each element in (-π, π)
            grad_ang %= TAU  # (-π, 0) is moved to (π, 2*π)

            self._grad_mag[oct_ind][layer_ind] = grad_mag
            self._grad_ang[oct_ind][layer_ind] = grad_ang

    def find_keypoints(self, keypoint_finder, n_max_per_layer):
        """
        Find keypoints and calculate the orientation with `keypoint_finder`
        """
        for oct_ind, layer_ind, kps in keypoint_finder(self, n_max_per_layer):
            self._keypoints[oct_ind][layer_ind] = kps

        n1 = self.n_keypoints
        self._add_orientation_to_keypoints()
        n2 = self.n_keypoints

        return n1, n2
        
    def _add_orientation_to_keypoints(self):
        """
        @return: a list with same length as keypoints,
            whose entry is a list containing main orientations of the keypoint with corresponding index.
            the orientation is expressed in radius in [0, 2π).

            It is possiable that the list is empty, implying orientation assignment failed due to
                sampling window exceeding the image boundary

            [
                [<orientation_0_of_keypoints_0>, <orientation_1_of_keypoints_0>, ..],
                [<orientation_0_of_keypoints_1>, <orientation_1_of_keypoints_1>, ..],
                ...
            ]
        """
        p_radi = para.sample_radius  # radius of sample reigon
        p_size = para.sample_size
        p_bins = para.orient_bins
        bin_to_ang = lambda i: i * (TAU / p_bins)

        def get_gaussian_kernel(layer_ind):
            sigma = get_sigma_by_layer(layer_ind)
            kernel = cv2_gaussian_kernel(p_size * 2 + 1, 1.5 * sigma)
            return kernel * kernel.T

        for oct_ind, layer_ind, layer, grad_mag, grad_ang, kps in self.full_enumerate():

            kp_with_ori = []
            rows, cols = layer.shape

            for kp in kps:

                r, c = int(kp[0]), int(kp[1])

                if not (p_radi <= r < rows - p_radi and p_radi <= c < cols - p_radi):
                    orients = []
                else:
                    region = (slice(r-p_size, r+p_size+1), slice(c-p_size, c+p_size+1))
                    angle_hist = hist(grad_ang[region], grad_mag[region] * get_gaussian_kernel(layer_ind), p_bins, TAU)
                    orients = [bin_to_ang(o) for o in arg_peaks(angle_hist, para.orient_threshold)]

                if not orients:
                    continue

                kp_with_ori.extend([kp + [o] for o in orients])

            self._keypoints[oct_ind][layer_ind] = kp_with_ori

    ##########################
    # Iteration tools
    ##########################
    def enumerate(self, target=None):
        if target is None:
            target = self._pyramid

        for i, j in product(range(self.n_octaves), range(self.n_layers_per_octave)):
            yield i, j, target[i][j]

    def full_enumerate(self):
        for i, j in product(range(self.n_octaves), range(self.n_layers_per_octave)):
            yield i, j, self._pyramid[i][j], self._grad_mag[i][j], self._grad_ang[i][j], self._keypoints[i][j]

