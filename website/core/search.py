# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-23 23:18:28
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-11 21:55:21
from __future__ import unicode_literals, print_function, division

from cv2 import imread as cv2_imread
from time import time
from functools import wraps

import numpy as np

from website.models import Logo
from website.database import db
from website.core.algorithm.utility import deserialize_floats
from website.core.search_text import get_search_func as get_text_search_func
from website.core.search_image import get_search_func as get_image_search_func
from website.core.search_tth import get_search_func as get_tth_search_func
from website.core.config import N_COLORS_MORE_THAN_SIX, LEVEL_NOT_REQUIRED, sat_level_check, val_level_check


def time_it(func):
    @wraps(func)
    def f(*args, **kwargs):
        t0 = time()
        ret = func(*args, **kwargs)
        t = time() - t0
        return ret, t

    return f

##########################
# Interface
##########################


class Searcher(object):

    def init(self):
        self._text_search = get_text_search_func()

        self._image_search_sift = get_image_search_func()
        self._image_search_color = get_tth_search_func()

        print("Searcher inited")

    def para_to_logo(self, para):
        para['filename'] = 'dataset/%s' % para['filename']
        para['theme_colors'] = para['theme_colors'].split()
        para['theme_weights'] = deserialize_floats(para['theme_weights'])
        return Logo(**para)

    def get_logos_from_db(self, inds):
        for i in inds:
            para = db.query("SELECT * FROM LOGOS WHERE IND = (%s)" % i)[0]
            # FIXME: hard code, not good
            yield self.para_to_logo(para)

    @time_it
    def text_search(self, keywords, ent_name="", n_colors=[],
                    saturation_levels=[], value_levels=[]):
        """
        Search logos by keywords

        @param: keywords : the characteristic of image, search from crawled data, may contain whitespaces as splits 
        @param: ent_name : the name of the enterprise, search from crawled data

        @param: n_colors : a list of number of main colors appeared in the logo image.
            The range of this value is defined in `core.config.py`, named `COLOR_SLOTS` and `COLOR_LEVEL`
            Where the first one denotes the upper bound of n_colors, 
            and `COLOR_LEVEL` denotes the resolution for each color channel in R,G,B.

        @param: saturation_levels, value_levels: a list of constants denoted the level of s,v values,
            defined in `website.core.config.py `, named something like 'SAT_LEVEL_LOW'

        @returns: one list of 'Logo' instance
        """
        if not hasattr(self, '_text_search'):
            self.init()

        ret = self._text_search(keywords=keywords, ent_name=ent_name)

        def check_ent_name(logo):
            if not ent_name:
                return True
            else:
                return ent_name in logo.ent_name

        def check_n_colors(logo):
            if not n_colors:
                return True
            elif N_COLORS_MORE_THAN_SIX in n_colors:
                return len(logo.theme_colors) in n_colors or len(logo.theme_colors) >= 6  # include 6
            else:
                return len(logo.theme_colors) in n_colors

        def check_sat(logo):
            if not saturation_levels:
                return True
            else:
                return any(sat_level_check(level, logo.s) for level in saturation_levels)

        def check_val(logo):
            if not value_levels:
                return True
            else:
                return any(val_level_check(level, logo.v) for level in value_levels)

        filters = lambda logo: all(f(logo) for f in (check_ent_name, check_n_colors, check_sat, check_val))

        ret = list(filter(filters, self.get_logos_from_db(ret)))
        return ret

    @time_it
    def image_search(self, path, threshold=0.7, max_n=50):
        """
        Search similar logos

        @param: path : the complete path to the image file
        @returns: two list of 'Logo' instance, where the first one contains good matches, and the second normal ones
        """
        im = cv2_imread(path)

        if im is None:
            print("No image at '%s' ,match failed!" % path)
            return [], []

        logo_inds_s, scores_s = self._image_search_sift(im, max_n=50)
        logo_inds_c, scores_c = self._image_search_color(im, max_n=50)

        print(logo_inds_c, logo_inds_s)
        print(scores_c, scores_s)
        scores = {}

        for ind, score in zip(logo_inds_s, scores_s):
            scores.setdefault(ind, 0)
            scores[ind] += score 
        
        for ind, score in zip(logo_inds_c, scores_c):
            scores.setdefault(ind, 0)
            scores[ind] += score

        # scores[logo_inds_s - mn] += scores_s ** 3 / 2
        # scores[logo_inds_c - mn] += scores_c ** 3 / 2
        # score = 0.5 * (score1 ** 2.5 + score2 ** 2.5)
        logo_inds = np.array(scores.keys())
        scores = np.array(scores.values())
        scores = (scores / 2) ** 0.5

        # get max_n
        max_n = min(np.sum(scores > threshold / 2), max_n)

        inds = np.argpartition(scores, -max_n)[-max_n:]
        inds = inds[np.argsort(scores[inds])][::-1]
        
        scores = scores[inds]
        logo_inds = logo_inds[inds] 

        print(logo_inds)
        print(scores)

        logo_inds += 1 # ind begins with 1
        logos = self.get_logos_from_db(logo_inds)

        good = []
        normal = []

        for logo, score in zip(logos, scores):
            (good if score > threshold else normal).append(logo)

        return good, normal
