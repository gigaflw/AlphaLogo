# -*- coding:utf-8 -*-
# Created by GigaFlower at 16/11/30
from __future__ import division, print_function
import cv2
import numpy as np
import os


def testset_generator(im):
    """
    Cast a variation of transform onto `im`, includes
            1. scale
            2. rotate
            3. affine
            4. gaussian blur
            5. reflect
    @yield: a tri-tuple
        (<name_of_the_transform>, <image_array>, <validation_function>)
        where <validation_function> is a function,
            receive a position (row, col), and return the new position after transform
    """
    def inner(m):
        return lambda r, c: np.dot(m, [c, r, 1])[::-1]

    rows, cols = im.shape
    
    # resize
    yield "scale1", cv2.resize(im, None, fx=0.5, fy=0.5), lambda r, c: (r/2, c/2)
    yield "scale2", cv2.resize(im, None, fx=2, fy=2), lambda r, c: (r*2, c*2)

    # rotate
    r_m1 = cv2.getRotationMatrix2D((cols/2, rows/2), -30, 1)
    yield "rotate_30", cv2.warpAffine(im, r_m1, (cols, rows)), inner(r_m1)

    r_m2 = cv2.getRotationMatrix2D((cols/2, rows/2), -45, 1)
    yield "rotate_45", cv2.warpAffine(im, r_m2, (cols, rows)), inner(r_m2)

    r_m3 = cv2.getRotationMatrix2D((cols/2, rows/2), -90, 1)
    yield "rotate_90", cv2.warpAffine(im, r_m3, (cols, rows)), inner(r_m3)
    
    # r_m4 = cv2.getRotationMatrix2D((cols/2, rows/2), -30, 0.7)
    # yield "rotate_30_scale_0.7", cv2.warpAffine(im, r_m4, (cols, rows)), inner(r_m4)    

    # r_m5 = cv2.getRotationMatrix2D((cols/2, rows/2), -30, 0.5)
    # yield "rotate_30_scale_0.5", cv2.warpAffine(im, r_m5, (cols, rows)), inner(r_m5)    

    # affine
    pts1 = np.array([[50, 50], [200, 50], [50, 200]], dtype=np.float32)
    pts2 = np.array([[10, 100], [200, 50], [100, 250]], dtype=np.float32)
    a_m = cv2.getAffineTransform(pts1, pts2)
    yield "affine", cv2.warpAffine(im, a_m, (cols, rows)), inner(a_m)

    # blur
    # yield "blur_11", cv2.GaussianBlur(im, (11, 11), 0), lambda r,c: (r,c)
    # yield "blur_31", cv2.GaussianBlur(im, (31, 31), 0), lambda r,c: (r,c)
    
    # reflect
    yield "reflect", im[:,::-1], lambda r,c : (r, cols-c)

def dataset_generator(dir_name):
    """
    @yield: all .jpg files in the specified directory `dir_name`
        (<filename>, <image_array>)
    """
    cnt = 0
    for filename in os.listdir(dir_name):
        if filename.endswith('jpg'):
            yield filename, cv2.imread(os.path.join(dir_name, filename), 0)
            if cnt > 30:
                return
            cnt += 1


def precision_test(matches, map_func, tolerance=3):
    """
    Judge how many matches are correct acoording to a function
    @param: matches:
        a bi-iterable [[<pos1_of_match_1>, <pos2_of_match_1>], [<pos1_of_match_2>, <pos2_of_match_2>], ...]
        where each `pos` is the position of the matching point like [<row>, <col>]
    @param: map_func:
        a function takes a position of the first image, return the corresponding position in the second
    @param: tolerance:
        matches with a error less than this value will be regarded as right 
        unit is pixel
    """
    def d(p1, p2):
        r1, c1 = p1
        r2, c2 = p2
        return ((r1-r2)**2 + (c1-c2)**2)**0.5

    if not matches:
        return 0.0

    pos1, pos2 = zip(*matches)
    r1, c1 = zip(*pos1)
    pos2_ = map(map_func, r1, c1)
    dis = [int(d(p2, p2_) <= tolerance) for p2, p2_ in zip(pos2, pos2_)]
    # [print(x) for x in list(zip(pos1, pos2, list(map(map_func, r1, c1)), dis))]

    return sum(dis) / len(dis)
