# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-01 20:51:30
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-07 15:42:08
#
# Helper function for search engine indexing
#
from __future__ import division, print_function

import math
import numpy as np
import cv2

from website.core.index.MMCQ import MMCQ

COLOR_LEVEL = 8
COLOR_SLOTS = 8
STYLE_0 = 0
STYLE_1 = 1
STYLE_2 = 2
STYLE_3 = 3
STYLE_4 = 4
STYLE_5 = 5
STYLE_6 = 6
STYLE_7 = 7
STYLE_8 = 8
STYLE_9 = 9
# to have better names


def get_theme_colors(im_name, color_level=8, color_slots=8):
    """
    From the image according to the given name,
    do
    1) search the image from `DATASET_DIR` from config.py
    2) compute the main colors by MMCQ algorithm, parametered by the same config file
    3) reduce the similiar colors returned
    4) compute color style

    @returns : (theme_colors, theme_weights, s_aver, v_aver), where
        theme_colors: a list of rgb colors, typed int
        theme_weights: a list of floats, sumed to 1
        s_aver: average value of 's' in hsv , ranged (0, 1)
        v_aver: average value of 'v' in hsv , ranged (0, 1)
    """
    # filename = full_path_dataset(im_name)
    im = cv2.imread(im_name)

    assert im is not None, "Empty image file '%s'" % im_name

    im = im[:, :, ::-1]  # BGR -> RGB
    colors = MMCQ(im, color_level, color_slots)
    colors, weights = zip(*colors)

    theme_colors, theme_weights = hsv_reduce_colors(colors, weights)

    # remove white backgrounds
    if len(theme_colors) > 2 and theme_weights[0] > 0.5 and theme_colors[0][2] >= 220:
        # print(colors, weights, theme_colors)
        print("white background ignored")
        colors, weights = colors[1:], weights[1:]

    aver, std = hsv_stat(colors, weights)
    s_aver, v_aver = aver[1], aver[2]

    # print(theme_colors, theme_weights, s_aver, v_aver)
    return theme_colors, theme_weights, s_aver, v_aver


def hsv_stat(colors, weights):
    """
    return values:
    (h_aver, s_aver, v_aver),(h_std, s_std, v_std)
    """
    colors = rgb_to_hsv(colors)
    hsv = colors / 255
    aver, std = np.average(hsv, axis=0, weights=weights), np.std(hsv, axis=0)
    return aver, std


def color_style_tag(colors, weights):
    """
    Compute style from a list of colors and weights according to hsv averages

    @param: colors: a list of RGB colors, typed uint8
    @param: weights: a list of floats

    @returns: a interger among `STYLE_X` constants denoting the style of color composition
    """
    colors = rgb_to_hsv(colors)
    sv = colors[:, 1:] / 255
    aver, std = np.average(sv, axis=0, weights=weights), np.std(sv, axis=0)
    print("s: %.5f %.5f" % (aver[0], std[0]), end='\t')
    print("v: %.5f %.5f" % (aver[1], std[1]))
    # range : aver : [0, 1], std: [0, 0.5]
    aver = (aver * 3).astype(np.int)  # discretization
    # range : aver : {1, 2, 3}  # 4 is ignored
    # raw_input('?')

    tag = aver[0] + aver[1] * 3

    return tag


def lab_reduce_colors(colors, threshold=30):
    """
    Reduce colors by L*a*b* space.
    """
    _colors = np.array([colors], dtype=np.uint8)  # cv2.cvtColor only accept 2d array
    lab_colors = cv2.cvtColor(_colors, cv2.COLOR_RGB2LAB)[0].astype(np.double)

    inds = []

    def euclidean(v1, v2):
        ret = ((v1-v2)**2).sum()**0.5
        return ret

    for i, color in enumerate(lab_colors):
        dist = ((lab_colors[inds] - color)**2).sum(axis=1)**0.5
        if not dist.size or dist.min() > threshold:
            inds.append(i)

    ret = _colors[0][inds]
    # print(len(ret))

    return ret


def hsv_reduce_colors(colors, weights, threshold=0.4):
    """
    Reduce colors into serveral main colors with HSV cone color space
    Requires:
        1) colors are sorted from 'color_with_more_pixels' to ''color_with_less_pixels''
        2) colors are in RGB color mode
        3) colors are int in [0, 255]

    @param: colors: a list
    >>> reduce_colors([[0,0,0],[255,255,255],[1,1,1],[25,25,25],[70,70,70]], threshold=70)
    [[0, 0, 0], [255, 255, 255], [70, 70, 70]]

    """
    hsv_colors = rgb_to_hsv(colors)
    hsv_colors /= [255/(2*np.pi), 255, 255]

    # to hsv cone color space
    h, s, v = np.split(hsv_colors, 3, axis=1)
    x, y, z = s * v * np.cos(h), s * v * np.sin(h), v
    hsv_colors_xyz = np.hstack([x, y, z])

    inds = []

    for i, color in enumerate(hsv_colors_xyz):
        # dist = ((hsv_colors_xyz[inds] - color)**2).sum(axis=1)**0.5
        dist = np.linalg.norm(hsv_colors_xyz[inds] - color, axis=1)
        if not dist.size or dist.min() > threshold:
            inds.append(i)

    ret = [colors[i] for i in inds]
    w = np.array(weights)[inds]
    w /= w.sum()
    # print(len(ret), ret)

    return ret, w


def to_web_color(color):
    """
    >>> to_web_color((255, 12, 67))
    '#ff0c43'
    """
    return '#{:02x}{:02x}{:02x}'.format(*color)


def rgb_to_hsv(colors):
    _colors = np.array([colors], dtype=np.uint8)  # cv2.cvtColor only accept 2d array
    hsv_colors = cv2.cvtColor(_colors, cv2.COLOR_RGB2HSV)[0].astype(np.double)

    return hsv_colors


def hsv_to_rgb(colors):
    _colors = np.array([colors], dtype=np.uint8)  # cv2.cvtColor only accept 2d array
    rgb_colors = cv2.cvtColor(_colors, cv2.COLOR_HSV2RGB)[0].astype(np.double)

    return rgb_colors
