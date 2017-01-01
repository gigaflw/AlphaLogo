# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-01 20:51:30
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-01 21:52:58
# 
# Helper function for search engine indexing
# 

import os
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
    file = os.path.join(IMAGE_PATH, im_name)
    im = imread(file)
    
    assert im is not None, "Empty image file '%s'" % im_name

    colors = MMCQ(im, COLOR_LEVEL, COLOR_SLOTS)
    colors = reduce_colors(colors)
    colors = list(map(to_web_color, colors))
    return colors

def reduce_colors(colors, threshold=70):
    """
    Reduce colors into serveral main colors
    Requires:
        1) colors are sorted from 'color_with_more_pixels' to ''color_with_less_pixels''
        2) colors have 3 channel, i.e. len(colors[i]) = 3
        3) colors are int in [0, 255]

    @param: colors: a list
    >>> reduce_colors([[0,0,0],[255,255,255],[1,1,1],[25,25,25],[70,70,70]], threshold=70)
    [[0, 0, 0], [255, 255, 255], [70, 70, 70]]
    """
    ret = []
    for color in colors:
        if not ret or \
            min(map(lambda c : euclidean_distance(c, color), ret)) > threshold:
            ret.append(color)

    return ret

def to_web_color(color):
    """
    >>> to_web_color((255, 12, 67))
    '#ff0c43'
    """
    return '#{:02x}{:02x}{:02x}'.format(*color)

def euclidean_distance(v1, v2):
    return sum(a**2 + b**2 for a,b in zip(v1,v2)) ** 0.5