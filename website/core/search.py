# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-23 23:18:28
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-09 13:46:42
from __future__ import unicode_literals, print_function

import os
from cv2 import imread as cv2_imread

from website.models import Logo
from website.database import db
from website.core.search_text import get_search_func as get_text_search_func
from website.core.search_image import get_search_func as get_image_search_func
# from website.core.search_image.color_match import get_search_func as get_image_search_func
from website.core.config import N_COLORS_MORE_THAN_SIX, LEVEL_NOT_REQUIRED, sat_level_check, val_level_check


##########################
# Interface
##########################
class Searcher(object):

    def init(self):
        self._text_search = get_text_search_func()
        self._image_search = get_image_search_func()
        print("Searcher inited")

    def para_to_logo(self, para):
        para['filename'] = os.path.join('dataset', para['filename'])
        para['theme_colors'] = para['theme_colors'].split()
        para['theme_weights'] = [int(w, base=16)/255.0 for w in para['theme_weights'].split()]
        return Logo(**para)

    def get_logos_from_db(self, inds):
        for i in inds:
            para = db.query("SELECT * FROM LOGOS WHERE IND = (%s)" % i)[0]
            # FIXME: hard code, not good
            yield self.para_to_logo(para)

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


    def _image_search(self, path):
        im = cv2_imread(path)

        if im is None:
            print("No image at '%s' ,match failed!" % path)
            return [], []

        logo_inds = self._image_search(im)
        logo_inds += 1  # ind begins with 1

        ret = list(self.get_logos_from_db(logo_inds))

        return [], ret

    
    def image_search(self, path, threshold=0.7):
        """
        Search similar logos

        @param: path : the complete path to the image file
        @returns: two list of 'Logo' instance, where the first one contains good matches, and the second normal ones
        """
        im = cv2_imread(path, 0)

        if im is None:
            print("No image at '%s' ,match failed!" % path)
            return [], []

        logo_inds, scores = self._image_search(im)
        logo_inds += 1  # ind begins with 1

        ret = self.get_logos_from_db(logo_inds)

        good = []
        normal = []

        for logo, score in zip(ret, scores):
            (good if score > threshold else normal).append(logo)


        return good, normal
