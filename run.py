# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-22 20:24:27
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-01 23:32:31

from website import app
from website.core.index import create_index

app.run(host='localhost', debug=True, threaded=True)
# create_index()
