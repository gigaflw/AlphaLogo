# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-22 20:23:50
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-22 21:01:41

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'
