# -*- coding:utf-8 -*-
# Created by GigaFlower at 16/12/16

from __future__ import division, print_function

import numpy as np
import cv2

from config import *


class KeypointFinder(object):

    def __call__(self, pyramid, **kwargs):
        """
        @param: pyramid : instance of `Pyramid` in `pyramid.py`
        @return: 
            A list of tuple with keypoints of type `Keypoint`
        [
            (octave_ind, layer_ind, [Keypoint1, Keypoint2, Keypoint3, ...])
            ....
        ]
        """
        raise NotImplementedError()


class CV2KeypointFinder(KeypointFinder):
    def __call__(self, pyramid, n_max):
        # f = 0
        for oct_ind, layer_ind, layer in pyramid.enumerate():
            # if f == 1:
                # yield oct_ind, layer_ind, []
            if layer_ind > 0:
                yield oct_ind, layer_ind, []
            else:
                # only the first layer
                yield oct_ind, layer_ind, self._find_in_image(layer, n_max)
                # f = 1

    def _find_in_image(self, image, n_max):
        """
        Calculate keypoints from a image
        Using cv2.goodFeaturesToTrack to find good points

        @param: image: np.ndarray
        @return: a list


        Cowards use this. The brave use '_key_points' which starts from scratch
        """
        rows, cols = image.shape
        kp = cv2.goodFeaturesToTrack(image, n_max, 0.01, 10, 3)
        # assert kp.shape = (<number of keypoints>, 1, 2)

        if kp is None:
            return []

        return [list(i) for i in kp.reshape(-1, 2)[:, ::-1].astype(np.int)]


class DoGKeypointFinder(KeypointFinder):
    def __init__(self):
        raise NotImplementedError()

    def _get_keypoints(self):
        assert self.pyramid

        DoG = self._DoG(self.pyramid)
        extrema = self._find_DoG_extrema(DoG)
        # todo: remove keypoints with low contrast
        # todo: remove keypoints at edge
        return extrema

    def _DoG(self, pyramid):
        """
        Contruct DoG ( Difference of Gaussian ) space from image pyramid P

            DoG[i][j] = P[i][j+1] - P[i][j]
        """

        # Calc DoG space
        DoG = []
        for octave in pyramid:
            octave = map(lambda layer: layer.astype(np.int16), octave)
            DoG.append(np.array([octave[i+1]-octave[i] for i in range(len(octave)-1)]))

        return DoG

    def _find_DoG_extrema(self, DoG):
        # TODO: sample ?
        ext = []
        for octave in DoG:
            _, rows, cols = octave.shape
            # assert octave.shape = (<layers>(=s+2), <rows>, <columns>)

            ##########################
            # time ?
            ##########################
            peeled = [octave[ind1, ind2, ind3] for ind1, ind2, ind3 in
                      product(*[[slice(1, -1), slice(2, None), slice(None, -2)]]*3)]
            center_block = peeled[0]  # octave[1:-1,1:-1,1:-1], the center part
            neighbor_blocks = peeled[1:]  # neighbors in 26 directions in 3-D DoG space with offset 1
            is_extreme = \
                np.bitwise_or(center_block > (np.max(neighbor_blocks, axis=0)),
                              center_block < (np.min(neighbor_blocks, axis=0)))
            # assert is_extreme.shape = (s, rows-2, columns-2)

            ext_coord = np.array(
                list(product(*[range(1, i-1) for i in octave.shape]))).reshape([x-2 for x in octave.shape]+[-1])
            assert ext_coord.shape[:-1] == is_extreme.shape

            ext_coord = ext_coord[is_extreme].astype(np.float)
            print("%d key point candidates found" % ext_coord.shape[0])
            # assert ext_coord.shape = (<number of key points>, 3)
            ext_coord /= [1, rows, cols]   # convert row, col coord to relative
            ext_coord[:, 0] = get_sigma_by_layer(ext_coord[:, 0])

            ext.extend(list(ext_coord))

            # filters
            # for layer, row, col in ext_coord:
            # nb = octave[layer-1:layer+2, row-1:row+2, col-1:col+2]  # 3x3x3 neighbor
            # x_hat, d_x_hat = self._fit_extremum(nb)
            # if
            # TODO: if x[i] > 0.5, do it recursivey
            # print(x_hat, d_x_hat)

        return ext

    @staticmethod
    def _fit_extremum(nb):
        """
        calc fitting point of extremum with a 3x3x3 neighborhood
        """
        assert nb.shape == (3, 3, 3)

        dx = (nb[1, 1, 2] - nb[1, 1, 0])/2
        dy = (nb[1, 2, 1] - nb[1, 0, 1])/2
        dl = (nb[2, 1, 1] - nb[0, 1, 1])/2

        dxx = (nb[1, 1, 2] - v) - (v - nb[1, 1, 0])
        dyy = (nb[1, 2, 1] - v) - (v - nb[1, 0, 1])
        dll = (nb[2, 1, 1] - v) - (v - nb[0, 1, 1])

        dxy = nb[1, 0, 0] + nb[1, 2, 2] - nb[1, 2, 0] - nb[1, 0, 2]
        dxl = nb[0, 1, 0] + nb[2, 1, 2] - nb[0, 1, 2] - nb[2, 1, 0]
        dyl = nb[0, 0, 1] + nb[2, 2, 1] - nb[2, 0, 1] - nb[0, 2, 1]

        grad = [dx, dy, dl]
        hessian = [[dxx, dxy, dxl], [dxy, dyy, dyl], [dxl, dyl, dll]]
        try:
            x_hat = - np.dot((np.linalg.inv(hessian)), grad)
            d_x_hat = v + 0.5 * np.dot(grad, x_hat)
            return x_hat, d_x_hat
        except:
            return [0, 0, 0], nb[1, 1, 1]
