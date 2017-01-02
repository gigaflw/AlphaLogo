# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-01 20:51:30
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-02 12:15:52
#
# Helper function for search engine indexing
#
from __future__ import division

import os
import math
from website.core.config import *
from website.core.index.MMCQ import MMCQ

from cv2 import imread


def theme_colors_for_web(im_name):
    """
    From the image according to the given name,
    do
    1) search the image from `IMAGE_PATH` from core.config.py
    2) compute the main the colors by MMCQ algorithm, parametered by the same config file
    3) reduce the similiar colors returned
    4) convert colors to web format (e.g. '#ff0c2a')
    5) return color strings 
    """
    file = os.path.join(IMAGE_MIRROR_DIR, im_name)
    im = imread(file)

    assert im is not None, "Empty image file '%s'" % im_name

    im = im[:, :, ::-1]  # BGR -> RGB
    colors = MMCQ(im, COLOR_LEVEL, COLOR_SLOTS)
    colors = reduce_colors(colors)
    colors = list(map(to_web_color, colors))
    return colors


def reduce_colors(colors, threshold=0.5):
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
    ret = []
    hsv = []
    for color in colors:
        # if not ret or \
        #         min(map(lambda c: euclidean_distance(c, color), ret)) > threshold:
        color_ = rgb_to_hsv(*color)
        if not ret or min(map(lambda c:hsv_distance(c, color_), hsv)) > threshold:
            ret.append(color)
            hsv.append(color_)

    return ret


def to_web_color(color):
    """
    >>> to_web_color((255, 12, 67))
    '#ff0c43'
    """
    return '#{:02x}{:02x}{:02x}'.format(*color)


def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0

    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn

    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360

    if mx == 0:
        s = 0
    else:
        s = df/mx

    v = mx

    return h, s, v


def euclidean_distance(v1, v2):
    return sum(a**2 + b**2 for a, b in zip(v1, v2)) ** 0.5


def hsv_distance(v1, v2):
    h1, s1, v1 = v1
    h2, s2, v2 = v2
    theta = (h1-h2) / 360 * math.pi
    return (s1**2 + s2**2 - 2 * s1 * s2 * math.cos(theta) + (v1 - v2)**2)**0.5
