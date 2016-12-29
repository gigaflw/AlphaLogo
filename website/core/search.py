# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-23 23:18:28
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-28 20:53:17
from __future__ import unicode_literals

import os

from website.models import Logo
from website.core.search_text import search as lucene_search  # can't load until lucene index is ready
from website.core.search_image import search as sift_search
from website.utility import save_img_to_uploads


##########################
# Interface
##########################
def text_search(keywords, ent_name=""):
    """
    Search logos by keywords

    @param: keywords : the characteristic of image, search from crawled data, may contain whitespaces as splits 
    @param: ent_name : the name of the enterprise, search from crawled data
    @returns: a list of 'Logo' instance
    """
    ret = lucene_search(keywords=keywords, ent_name=ent_name)

    def para_to_logo(para):
        para['filename'] = os.path.join('dataset', para['filename'])
        return Logo(**para)

    def is_good_match(logo):
        """
        Find out good matches
        To be intensified
        """
        if ent_name and ent_name in logo.ent_name:
            return True
        else:
            return False

    good = []
    normal = []

    for l in map(para_to_logo, ret):
        (good if is_good_match(l) else normal).append(l)

    return good, normal


def image_search(im):
    """
    Search similar logos

    @param: im : a `werkzeug.datastructures.FileStorage` instance
    @returnsL a list of `Logo` instance, sorted in the order of similarity
    """
    # path = save_img_to_uploads(im)
    # logos = sift_search(path)

    # fake data
    logos = [
        Logo(os.path.join('dataset', 'demo', '1.jpg'), '手持一把锟斤拷，口中疾呼烫烫烫'),
        Logo(os.path.join('dataset', 'demo', '2.jpg'), '问天再借五百年'),
        Logo(os.path.join('dataset', 'demo', '3.jpg'), 'A quick brown fox jumps over the lazy dog'),
        Logo(os.path.join('dataset', 'demo', '4.jpg'), '大美兴，川普王'),
        Logo(os.path.join('dataset', 'demo', '5.jpg'), '黄焖鸡米饭')
    ]
    return logos
