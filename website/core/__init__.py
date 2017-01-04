# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-23 23:18:15
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-04 12:54:52

from website.core.search import Searcher

searcher = Searcher()
text_search = searcher.text_search
image_search = searcher.image_search
init_searcher = searcher.init
