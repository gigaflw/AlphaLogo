# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-22 20:23:50
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-23 23:06:19

from flask import Flask

from website.views import bp

app = Flask(__name__)

app.register_blueprint(bp)

