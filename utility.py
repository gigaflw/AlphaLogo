# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-01 20:51:30

from __future__ import division
import math


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


def hsv_distance(v1, v2):
    h1, s1, v1 = v1
    h2, s2, v2 = v2
    theta = (h1-h2) / 360 * math.pi
    return (s1**2 + s2**2 - 2 * s1 * s2 * math.cos(theta) + (v1 - v2)**2)**0.5
