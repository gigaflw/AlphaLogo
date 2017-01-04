# -*- coding:utf-8 -*-
# Created by GigaFlower at 16/11/30
from __future__ import division

import numpy as np

PI = np.pi
TAU = 2 * np.pi


def hist(values, weights, bins, max_val):
    """
    !!! Time consuming !!!!

    Construct the histogram of `values` according to `weights`
    The value of `values` should be positive

    @returns:
        [<sum_of_weights_for_values_in_bin_0>, <sum_of_weights_for_values_in_bin_1>, ...]
    """
    # assert values.shape == weights.shape

    values = np.round(values / max_val * bins) % bins
    hist = [np.sum(weights[values == i]) for i in range(bins)]

    return hist


def arg_peaks(hist, ratio):
    """
    Return the indicies whose value > ratio * hist.max()
    e.g.
        arg_peaks([0,9,0,9,0,9,0,9,10], 0.8)
        -> [1,3,5,7,8]
    """
    if not len(hist):  # hist may be np.ndarray
        return []

    m = max(hist)
    tmp = (i if x > m*ratio else None for i, x in enumerate(hist))

    return filter(lambda x: x is not None, tmp)


def arg_valley(hist, ratio):
    if not len(hist):  # hist may be np.ndarray
        return []

    m = min(hist)
    tmp = (i if x < m/ratio else None for i, x in enumerate(hist))

    return filter(lambda x: x is not None, tmp)


def double_interpolation(layer, row, col):
    """
    !!! Very time consuming !!!!
    Guess irresponsibly layer[row,col] where `row` and `col` are floats
    """

    bc, br = int(col), int(row)

    dc = col - bc
    dr = row - br
    p = dc * dr

    neighbor = layer[
        [br, br, br+1, br+1],
        [bc, bc+1, bc, bc+1]
    ]
    # val = np.sum(neighbor * [dr*dc, dr*(1-dc), (1-dr)*dc, (1-dr)*(1-dc)])
    val = np.sum(neighbor * [p, dr-p, dc-p, 1-dr-dc+p])

    return val


def hsv_to_rgb(h, s, v):
    h = h % 360

    hi = h//60
    f = h/60.0 - hi
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1-f) * s)

    if hi == 0:
        return v, t, p
    elif hi == 1:
        return q, v, p
    elif hi == 2:
        return p, v, t
    elif hi == 3:
        return p, q, v
    elif hi == 4:
        return t, p, v
    elif hi == 5:
        return v, p, q
