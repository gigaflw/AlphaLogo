# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-23 23:18:28
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-25 11:05:07
from __future__ import unicode_literals

import os

from website.core.sift import sift
from website.core.lucene import search as lucene_search

from collections import namedtuple
Logo = namedtuple('Logo', ['filename', 'ent_name'])

##########################
# Interface
##########################
def text_search(kw):
    """
    Search function

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
    pass


