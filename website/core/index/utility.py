# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-01 20:51:30
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-06 21:48:00
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
    2) compute the main the colors by MMCQ algorithm, parametered by the same config file
    3) reduce the similiar colors returned
    4) convert colors to web format (e.g. '#ff0c2a')
    5) return color strings 
    """
    # filename = full_path_dataset(im_name)
    im = cv2.imread(im_name)

    assert im is not None, "Empty image file '%s'" % im_name

    im = im[:, :, ::-1]  # BGR -> RGB
    colors = MMCQ(im, color_level, color_slots)
    colors, weights = zip(*colors)

    theme_colors = hsv_reduce_colors(colors)
    
    # remove white backgrounds
    if len(theme_colors) > 2 and weights[0] > 0.1 and theme_colors[0][2] >= 220:
        print("white background ignored")
        colors, weights = colors[1:], weights[1:]
        theme_colors = theme_colors[1:]

    color_style = color_style_tag(colors, weights)

    # print(theme_colors, color_style)
    return theme_colors, color_style


def color_style_tag(colors, weights):
    colors = rgb_to_hsv(colors)
    sv = colors[:,1:] / 255
    aver, std = np.average(sv, axis=0, weights=weights), np.std(sv, axis=0)
    # print("s: %.5f %.5f" % (aver[0], std[0]), end='\t')
    # print("v: %.5f %.5f" % (aver[1], std[1]))
    # range : aver : [0, 1], std: [0, 0.5]
    aver = (aver * 3).astype(np.int)  # discretization
    # range : aver : {1, 2, 3}  # 4 is ignored
    # raw_input('?')


    tag = aver[0] + aver[1] * 3

    return tag



def _color_style_tag(im_name, std_threshold=1):
    filename = full_path_dataset(im_name)
    im = cv2.imread(filename)

    assert im is not None, "Empty image file '%s'" % im_name
    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    hsv = im.reshape((-1, 3))
    hsv = np.vstack({tuple(row) for row in hsv})  # remove duplicated values to avoid background influence

    sv = hsv[:,1:].astype(np.double) / 255
    # hue component is ignored

    aver, std = np.average(sv, axis=0), np.std(sv, axis=0)
    print(im_name, end='\t')
    print("s: %.5f %.5f" % (aver[0], std[0]), end='\t')
    print("v: %.5f %.5f" % (aver[1], std[1]))
    print(sv)
    # range : aver : [0, 1], std: [0, 0.5]
    aver = (aver * 3).astype(np.int) + 1  # discretization
    # range : aver : {1, 2, 3}  # 4 is ignored
    raw_input('?')

    if sum(std) > std_threshold:
        tag = STYLE_0
    else:
        tag = aver[0] + aver[1] * 3

    return tag


def lab_reduce_colors(colors, threshold=30):
    _colors = np.array([colors], dtype=np.uint8)  # cv2.cvtColor only accept 2d array
    lab_colors = cv2.cvtColor(_colors, cv2.COLOR_RGB2LAB)[0].astype(np.double)

    inds = []
    # euclidean = lambda v1,v2: ((v1-v2)**2).sum()**0.5

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


def hsv_reduce_colors(colors, threshold=0.35):
    """
    Reduce colors into serveral main colors
    Requires:
        1) colors are sorted from 'color_with_more_pixels' to ''color_with_less_pixels''
        2) colors have 3 channel, i.e. len(colors[i]) = 3
        3) colors are int in [0, 255]

    @param: colors: a list
    >>> reduce_colors([[0,0,0],[255,255,255],[1,1,1],[25,25,25],[70,70,70]], threshold=70)
    [[0, 0, 0], [255, 255, 255], [70, 70, 70]]

    # TODO: Not a good algorithm
    """
    hsv_colors = rgb_to_hsv(colors)
    hsv_colors /= [255/(2*np.pi), 255, 255]

    # to hsv cone color space
    h, s, v = np.split(hsv_colors, 3, axis=1)
    x, y, z = s * v * np.cos(h), s * v * np.sin(h), v
    hsv_colors_xyz = np.hstack([x, y, z])
    # print(hsv_colors_xyz)

    inds = []

    for i, color in enumerate(hsv_colors_xyz):
        dist = ((hsv_colors_xyz[inds] - color)**2).sum(axis=1)**0.5
        if not dist.size or dist.min() > threshold:
            inds.append(i)

    ret = [colors[i] for i in inds]
    # print(len(ret), ret)
    # raw_input('?')

    return ret


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
