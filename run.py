# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-22 20:24:27
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-04 13:09:54

from website import app
from website.core import init_searcher

init_searcher()
app.run(host='localhost', debug=True, threaded=True)
