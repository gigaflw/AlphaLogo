# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-23 23:18:15
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-12 21:00:49
# 
# Service logics and algorithms
# 

from website.core.search import Searcher

_searcher = Searcher()
text_search = _searcher.text_search
image_search = _searcher.image_search
init_searcher = _searcher.init
