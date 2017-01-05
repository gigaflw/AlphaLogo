# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-23 23:18:28
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-05 18:55:37
from __future__ import unicode_literals, print_function

import os
from cv2 import imread as cv2_imread

from website.models import Logo
from website.database import db
from website.core.search_text import get_search_func as get_text_search_func
from website.core.search_image import get_search_func as get_image_search_func
from website.core.config import N_COLORS_MORE_THAN_SIX
from website.utility import save_img_to_uploads


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
        return Logo(**para)

    def get_logos_from_db(self, inds):
        for i in inds:
            para = db.query("SELECT FILENAME, ENT_NAME, INFO, THEME_COLORS FROM LOGOS WHERE IND = (%s)" % i)[0]
            # FIXME: hard code, not good
            yield self.para_to_logo(para)

    def text_search(self, keywords, ent_name="", n_colors=[]):
        """
        Search logos by keywords

        @param: keywords : the characteristic of image, search from crawled data, may contain whitespaces as splits 
        @param: ent_name : the name of the enterprise, search from crawled data

        @param: n_colors : a list of number of main colors appeared in the logo image.
            The range of this value is defined in `core.config.py`, named `COLOR_SLOTS` and `COLOR_LEVEL`
            Where the first one denotes the upper bound of n_colors, 
            and `COLOR_LEVEL` denotes the resolution for each color channel in R,G,B.

        @returns: two list of 'Logo' instance, where the first one contains good matches, and the second normal ones
        """
        if not hasattr(self, '_text_search'):
            self.init()

        ret = self._text_search(keywords=keywords, ent_name=ent_name)

        def is_good_match(logo):
            """
            Find out good matches
            To be intensified
            """
            if ent_name and ent_name in logo.ent_name:
                return True
            else:
                return False

        if N_COLORS_MORE_THAN_SIX in n_colors:
            check_n_color = lambda logo: len(logo.theme_colors) in n_colors or len(logo.theme_colors) >= 6
        else:
            check_n_color = lambda logo: len(logo.theme_colors) in n_colors

        good = []
        normal = []

        for l in filter(check_n_color, self.get_logos_from_db(ret)):
            (good if is_good_match(l) else normal).append(l)

        return good, normal

    def image_search(self, im):
        """
        Search similar logos

        @param: im : a `werkzeug.datastructures.FileStorage` instance
        @returns: two list of 'Logo' instance, where the first one contains good matches, and the second normal ones
        """
        path = save_img_to_uploads(im)
        im = cv2_imread(path, 0)

        if im is None:
            print("Empty image to search!")
            return [], []

        logo_inds = self._image_search(im) + 1  # ind begins with 1

        ret = list(self.get_logos_from_db(logo_inds))

        return ret[:1], ret[1:]
