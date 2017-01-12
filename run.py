# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-22 20:24:27
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-12 20:42:01

from website import create_app

app = create_app()
app.run(host='localhost', debug=True, threaded=False)
