# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-23 23:18:28
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-25 15:23:43
from __future__ import unicode_literals

import os

from website.models import Logo
# from website.core.search_text import search as lucene_search  # can't load until lucene index is ready
from website.core.search_image import search as sift_search
from website.utility import save_img_to_uploads


##########################
# Interface
##########################
def text_search(kw):
    """
    Search logos by keywords

    @param: kw : a string, the keywords
    @returns: a list of info on matched images
    """

    # fake data
    logos = [
        Logo(os.path.join('dataset', 'demo', '1.jpg'), '手持一把锟斤拷，口中疾呼烫烫烫'),
        Logo(os.path.join('dataset', 'demo', '2.jpg'), '问天再借五百年'),
        Logo(os.path.join('dataset', 'demo', '3.jpg'), 'A quick brown fox jumps over the lazy dog'),
        Logo(os.path.join('dataset', 'demo', '4.jpg'), '大美兴，川普王'),
        Logo(os.path.join('dataset', 'demo', '5.jpg'), '黄焖鸡米饭')
    ]
    return logos


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
