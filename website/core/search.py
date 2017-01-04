# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-23 23:18:28
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-04 16:56:51
from __future__ import unicode_literals, print_function

import os
from cv2 import imread as cv2_imread

from website.models import Logo
from website.database import db
from website.core.search_text import get_search_func as get_text_search_func
from website.core.search_image import get_search_func as get_image_search_func
from website.utility import save_img_to_uploads


##########################
# Interface
##########################
class Searcher(object):

    def init(self):
        self.lucene_search = get_text_search_func()
        self._image_search = get_image_search_func()
        print("Searcher inited")

    def para_to_logo(self, para):
        para['filename'] = os.path.join('dataset', para['filename'])
        para['theme_colors'] = para['theme_colors'].split()
        return Logo(**para)

    def text_search(self, keywords, ent_name="", n_colors=""):
        """
        Search logos by keywords

        @param: keywords : the characteristic of image, search from crawled data, may contain whitespaces as splits 
        @param: ent_name : the name of the enterprise, search from crawled data

        @param: n_colors : number of main colors appeared in the logo image.
            The range of this value is defined in `core.config.py`, named `COLOR_SLOTS` and `COLOR_LEVEL`
            Where the first one denotes the upper bound of n_colors, 
            and `COLOR_LEVEL` denotes the resolution for each color channel in R,G,B.

        @returns: a list of 'Logo' instance
        """
        if not hasattr(self, 'lucene_search'):
            self.init()

        ret = self.lucene_search(keywords=keywords, ent_name=ent_name, n_colors=n_colors)

        def is_good_match(logo):
            """
            Find out good matches
            To be intensified
            """
            if (ent_name and ent_name in logo.ent_name) and \
                    (n_colors == '' or abs(int(n_colors) - len(logo.theme_colors)) <= 1):
                return True
            else:
                return False

        good = []
        normal = []

        ret = db.query("SELECT FILENAME, ENT_NAME, INFO, THEME_COLORS FROM LOGOS WHERE IND IN (%s)" %
                       ','.join(map(str, ret)))
        for l in map(self.para_to_logo, ret):
            (good if is_good_match(l) else normal).append(l)

        return good, normal

    def image_search(self, im):
        """
        Search similar logos

        @param: im : a `werkzeug.datastructures.FileStorage` instance
        @returnsL a list of `Logo` instance, sorted in the order of similarity
        """
        if not hasattr(self, '_image_search'):
            self.init()

        path = save_img_to_uploads(im)
        im = cv2_imread(path, 0)
        assert im is not None, "Empty image to search!"
        logo_inds = self._image_search(im) + 1

        ret = db.query("SELECT FILENAME, ENT_NAME, INFO, THEME_COLORS FROM LOGOS WHERE IND IN (%s)" %
                       ','.join(map(str, logo_inds)))
        ret = list(map(self.para_to_logo, ret))

        return ret[:1], ret[1:]
