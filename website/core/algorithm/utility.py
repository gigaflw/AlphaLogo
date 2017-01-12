# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-01 20:51:30
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-12 21:26:11
#
# Helper function for search engine indexing
#
from __future__ import division, print_function

import math
import numpy as np
import cv2

from website.core.algorithm import MMCQ


def get_theme_colors(im_name, color_level=8, color_slots=8):
    """
    From the image according to the given name,
    do
    1) search the image from `DATASET_DIR` from config.py
    2) compute the main colors by MMCQ algorithm, parametered by the same config file
    3) reduce the similiar colors returned
    4) compute hsv stat

    @returns : (theme_colors, theme_weights, s_aver, v_aver), where
        theme_colors: a list of rgb colors, typed int
        theme_weights: a list of floats, sumed to 1
        s_aver: average value of 's' in hsv , ranged (0, 1)
        v_aver: average value of 'v' in hsv , ranged (0, 1)
    """
    im = cv2.imread(im_name)
    assert im is not None, "Empty image file '%s'" % im_name


    im = im[:, :, ::-1]  # BGR -> RGB
    colors = MMCQ(im, color_level, color_slots)
    colors, weights = zip(*colors)
    colors = np.array(colors)

    theme_colors, theme_weights = hsv_reduce_colors(colors, weights)

    # remove white backgrounds
    if len(theme_colors) > 2 and theme_weights[0] > 0.5 and theme_colors[0][2] >= 220:
        print("white background ignored")
        # colors, weights = colors[1:], weights[1:]

    aver, std = hsv_stat(colors, weights)
    s_aver, v_aver = aver[1], aver[2]

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


def serialize_colors(colors):
    """
    [[255, 255, 255], [255, 0, 0]] -> '#ffffff #ff0000'
    """
    return " ".join(map(to_web_color, colors))

def deserialize_colors(color_string):
    pass

def serialize_floats(floats):
    """
    [1, 0, 0.2] -> "ff 00 33"
    """
    return " ".join("%02x" % (x*255) for x in floats)

def deserialize_floats(float_string):
    """
    "ff 00 33" -> [1, 0, 0.2]
    """
    return [int(f, base=16)/255.0 for f in float_string.split()]


def lab_reduce_colors(colors, weights,  threshold=30, return_rgb=True):
    """
    Reduce colors by L*a*b* space.
    """
    _colors = np.array([colors], dtype=np.uint8)  # cv2.cvtColor only accept 2d array
    lab_colors = cv2.cvtColor(_colors, cv2.COLOR_RGB2LAB)[0].astype(np.double)

    inds = []

    for i, color in enumerate(lab_colors):
        dist = np.linalg.norm(hsv_colors_xyz[inds] - color, axis=1)
        if not dist.size or dist.min() > threshold:
            inds.append(i)

    if return_rgb:
        ret = colors[inds]
    else:
        ret = lab_colors[inds]

    return ret


def hsv_reduce_colors(colors, weights, threshold=0.4, return_rgb=True):
    """
    Reduce colors into serveral main colors with HSV cone color space
    Requires:
        1) colors are sorted from 'color_with_more_pixels' to ''color_with_less_pixels''
        2) colors are in RGB color mode
        3) colors are int in [0, 255]

    @param: colors: a list
    >>> reduce_colors([[0,0,0],[255,255,255],[1,1,1],[25,25,25],[70,70,70]], threshold=70)
    [[0, 0, 0], [255, 255, 255], [70, 70, 70]]

    @param: return_rgb:
        returned color is in RGB mode if `True`
        else hsv mode

    @return:
        the result colors and their weights
    """
    hsv_colors = rgb_to_hsv(colors)
    hsv_colors /= 255

    # to hsv cone color space
    h, s, v = np.split(hsv_colors, 3, axis=1)
    x, y, z = s * v * np.cos(h), s * v * np.sin(h), v
    hsv_colors_xyz = np.hstack([x, y, z])

    inds = []

    for i, color in enumerate(hsv_colors_xyz):
        dist = np.linalg.norm(hsv_colors_xyz[inds] - color, axis=1)
        if not dist.size or dist.min() > threshold:
            inds.append(i)

    if return_rgb:
        ret = colors[inds]
    else:
        ret = hsv_colors[inds]

    w = np.array(weights)[inds]
    w /= w.sum()

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


