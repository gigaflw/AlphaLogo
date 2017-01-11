# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-07 20:39:08
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-09 14:06:25

from __future__ import division
import math
import pickle
import cv2
import numpy as np

from website.core.config import IMAGE_INDEX_TTH_FILE


def get_search_func():
    with open(IMAGE_INDEX_TTH_FILE, 'rb') as f:
        data = pickle.load(f)
        print("TTH data load.")

    def match(im, max_n=50):
        vector = vectorize(im)
        scores = np.array([get_grade(vector, d)[1] for d in data])
        # the smaller, the better

        ret = np.argpartition(scores, max_n)[:max_n]
        ret = ret[np.argsort(scores[ret])]
        print("TTH find match inds(begin with 0):\t", ret)
        print("Their scores(smaller is better):\t", scores[ret])

        return ret, scores[ret]

    return match


def vectorize(im):
    a = find_maincolor(im)
    b = find_number(a, im)
    vector = brief(a, b, im)

    return vector


def get_grade(v1, v2):  # 比较的两个图像特征向量
    # shape: [[(h1,s1,v1), w1], [(h2,s2,v2), w2], ...]
    # h : 0 ~ 360
    # s,v: 0 ~ 1
    # return: [background_score, logo_score]

    x = [0, 0]

    hsv1, w1 = zip(*v1)
    hsv2, w2 = zip(*v2)

    hsv1 = np.array(hsv1, dtype=np.double)
    hsv2 = np.array(hsv2, dtype=np.double)

    hsv1[:, 0] /= 360
    hsv2[:, 0] /= 360

    # background
    # m = hsv2[-1] - hsv1[-1]  # -1 is background
    # x[0] = math.exp(-np.linalg.norm(m))

    # logo body
    def delta(_v1, _w1, _v2, _w2):
        return math.exp(np.linalg.norm(_v1-_v2) + 100 * (_w1-_w2)**2) * (_w1 * 100)

    for i in range(len(hsv1) - 1):
        y = [delta(hsv1[i], w1[i], hsv2[j], w2[j]) for j in range(len(hsv2) - 1)]
        x[1] += min(y)

    return x


def find_maincolor(src):
    b = []

    for i in range(0, src.shape[0], 10):
        for j in range(0, src.shape[1], 10):
            color = src[i, j].astype(np.int)

            flag = True
            for k in range(len(b)):
                if np.linalg.norm(color - b[k]) < 37:
                    flag = False

            if flag:
                b.append(color)

    return b


def find_number(center_point, img):
    number = [0] * len(center_point)

    for i in range(0, img.shape[0], 2):
        for j in range(0, img.shape[1], 2):

            color = img[i, j].astype(np.int)

            vector = [0] * len(center_point)

            for k in range(len(center_point)):
                a = center_point[k] - color
                vector[k] = np.dot(a, a.T)

            temp = np.argmin(vector)
            number[temp] = number[temp] + 1

    for i in range(len(number)):
        number[i] = 4 * number[i] / (img.shape[0]*img.shape[1])

    return number


def brief(a, b, img):
    new_vector = []

    for i in range(len(a)):

        color = rgb_to_hsv(*a[i][::-1])
        new_vector.append([color, b[i]])

    bg_color = rgb_to_hsv(*img[1, 1][::-1])

    new_vector.append([bg_color, 1])
    new_vector = sorted(new_vector, key=lambda x: x[1], reverse=True)

    while new_vector[-1][1] < 0.01 and len(new_vector) > 4:
        del new_vector[-1]

    new_vector = new_vector[::-1]

    # for i in range(len(new_vector)-1, 0, -1):
    # if new_vector[i][1] < 0.01 and len(new_vector) > 4:
    # del new_vector[len(new_vector)-1]

    # new_vector = sorted(new_vector, key=lambda x: x[1])

    return new_vector


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

if __name__ == '__main__':
    match(0)
