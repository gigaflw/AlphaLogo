# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-23 23:18:28
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-01 23:41:54
from __future__ import unicode_literals, print_function

import os

from website.models import Logo
from website.core.search_text import get_search_func as get_text_search_func
# from website.core.search_image import search as sift_search
from website.utility import save_img_to_uploads


##########################
# Interface
##########################
class Searcher(object):
    def init(self):
        self.lucene_search = get_text_search_func()

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

        def para_to_logo(para):
            para['filename'] = os.path.join('dataset', para['filename'])
            para['theme_colors'] = para['theme_colors'].split()
            return Logo(**para)

        def is_good_match(logo):
            """
            Find out good matches
            To be intensified
            """
            if (ent_name == '' or ent_name in logo.ent_name) and \
                (n_colors == '' or abs(int(n_colors) - len(logo.theme_colors)) <= 1):
                return True
            else:
                return False

        good = []
        normal = []

        for l in map(para_to_logo, ret):
            (good if is_good_match(l) else normal).append(l)

        return good, normal

    @staticmethod
    def image_search(im):
        """
        Search similar logos

        @param: im : a `werkzeug.datastructures.FileStorage` instance
        @returnsL a list of `Logo` instance, sorted in the order of similarity
        """
        # path = save_img_to_uploads(im)
        # logos = sift_search(path)

        # fake data
        logos = []
        for fname, info, ent_name in [
            (os.path.join('dataset', 'demo', '1.jpg'), '手持一把锟斤拷，口中疾呼烫烫烫', '测试1'),
            (os.path.join('dataset', 'demo', '2.jpg'), '问天再借五百年', '测试2'),
            (os.path.join('dataset', 'demo', '3.jpg'), 'A quick brown fox jumps over the lazy dog', '测试3'),
            (os.path.join('dataset', 'demo', '4.jpg'), '大美兴，川普王', '测试4'),
            (os.path.join('dataset', 'demo', '5.jpg'), '黄焖鸡米饭', '测试5')
        ]:
            logos.append(Logo(fname, info, ent_name, "#000000"))
        good = [logos[0]]
        normal = logos[1:]

        return good, normal
