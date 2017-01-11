# -*- coding:utf-8 -*-
# Created by GigaFlower at 16/12/16

from itertools import product

import numpy as np
import cv2

from util import *
from config import *

cv2_gaussian_kernel = cv2.getGaussianKernel

p_n = para.descr_n
p_s = para.descr_size
p_b = para.descr_bins

class DescriptorMatcher:

    def __call__(self, descriptor1, descriptor2):
        """
        @yield: (i, j) pairs which means i-th keypoint in d1 matches with j-th keypoint in d2

        @param: d1: a np.ndarray containing descriptors of image1
            with shape (<number_of_keypoints_1>, <length_of_descriptor>)
        @param: d2: a np.ndarray containing descriptors of image2
            with shape (<number_of_keypoints_2>, <length_of_descriptor>)

        calc res = np.dot(d1, d2.T)
        than res_ij is the resemblance between keypoint_i in image1 and keypoint_j in image2

        If in one row of res, the max value * 0.8 >  the secondly max value, a success match is found

        """
        assert descriptor1.shape[1] == descriptor2.shape[1], "Desciptors must have same vector length to match!"

        # print(np.round(descriptor1[7], 3))
        # print(np.round(descriptor2[1], 3))
        # print(np.dot(descriptor2[1], descriptor1[7]))

        # for i in range(16):
            # if i not in [6,9]:
                # continue
            # print(np.dot(descriptor2[1][i*8:(i+1)*8], descriptor1[7][i*8:(i+1)*8]))


        resem = np.dot(descriptor1, descriptor2.T)
        resem = np.sqrt(1 + 1e-10 - resem)


        cnt = [0, 0, 0]
        ret = []

        for i, row in enumerate(resem):
            peaks = arg_valley(row, para.descr_match_contrast)
            # assert len(peaks) > 1
            # for p in peaks:
                # yield i,p
            if len(peaks) == 0:
                raise ValueError, "Can't find peak in empty list. Something wrong happens!"
            elif len(peaks) > 1:
                # for p in peaks:
                    # ret.append((i, p, row[p]))
                    # print(i, p, row[p])
                cnt[1] += 1
            elif row[peaks[0]] > para.descr_match_threshold:
                cnt[2] += 1
            else:
                cnt[0] += 1
                ret.append((i, peaks[0], row[peaks[0]]))

        return ret, cnt


class DescriptorCalculator:
    coord_seed = np.split(np.arange(0.5 - p_s * p_n // 2, p_s * p_n // 2), p_n)
    region_index = list(product(range(p_n), range(p_n)))
    region_n = p_n * p_n
    coords = [list(product(coord_seed[i], coord_seed[j])) for i, j in region_index]

    def __call__(self, pyramid, use_biliner_interpolation):
        descriptors = []
        positions = []
        dp_add = descriptors.append
        pos_add = positions.append

        for octave_ind, layer_ind, layer, grad_mag, grad_ang, kps in pyramid.full_enumerate():
            
            scale = get_scale_by_ind(octave_ind, layer_ind)
            ratio = get_size_ratio_by_octave(octave_ind)

            gaussian_kernel = cv2_gaussian_kernel(p_s * p_n, para.descr_gaussian_ratio * scale)
            kernels = [gaussian_kernel[i*p_s:(i+1)*p_s] * gaussian_kernel[j*p_s:(j+1)*p_s].T for i, j in self.region_index]

            for row, col, ori in kps:
                dp = self.calc(row, col, ori, grad_mag, grad_ang, kernels, use_biliner_interpolation)
                dp_add(dp)
                pos_add([row / ratio, col / ratio])

        if descriptors:
            return np.stack(descriptors), np.array(positions, dtype=np.int)
        else:
            return np.array([[]]), np.array([[]])


    def calc(self, row, col, ori, grad_mag, grad_ang, kernels, use_biliner_interpolation):
        descriptor = []

        for ind in range(self.region_n):

            kernel = kernels[ind]
            rotated = self._rotate(-ori, self.coords[ind])

            # double linear interpolation
            if use_biliner_interpolation:
                mag_hat = np.array([double_interpolation(grad_mag, y+row, x+col) for x, y in rotated]).reshape(p_s, p_s)
                ang_hat = np.array([double_interpolation(grad_ang, y+row, x+col) for x, y in rotated]).reshape(p_s, p_s)
            else:
                rotated += [col, row]  # relative to object -> relative to layer
                rotated = np.array([(round(r), round(c)) for (c,r) in rotated], dtype=int)
                mat_ind = np.split(rotated, 2, axis=1)
                mag_hat = grad_mag[mat_ind].reshape(p_s, p_s)
                ang_hat = grad_ang[mat_ind].reshape(p_s, p_s)

            ang_hat = (ang_hat - ori) % TAU
            angle_hist = hist(ang_hat, mag_hat * kernel, p_b, TAU)
            descriptor.extend(angle_hist)

            # cv2.circle(layer, (rotated[0][0], rotated[0][1]), 2, (255*ind/16, 255*ind/16, 255*ind/16), 2)

        descriptor = np.array(descriptor)
        norm = np.sum(descriptor**2)**0.5

        return descriptor / norm

    @staticmethod
    def _rotate(ang, coord_mat):
        """each row vector in `vec` represents a 2D coord"""
        s, c = np.sin(ang), np.cos(ang)
        rot_mat = [[c, -s], [s, c]]
        return np.dot(coord_mat, rot_mat)
