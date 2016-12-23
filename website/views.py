# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-22 20:25:31
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-23 23:26:03

from flask import Blueprint, render_template, abort, flash

from core import search 


bp = Blueprint('bp', __name__, template_folder='templates')

@bp.route('/')
def hello_world():
    return render_template('index.html')

@bp.route('/search')
def search():
    return render_template('search.html')
