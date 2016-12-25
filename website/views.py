# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-22 20:25:31
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-25 10:26:02

from flask import Blueprint, render_template, abort, request

from website.core import image_search, text_search

bp = Blueprint('bp', __name__, template_folder='templates')

@bp.route('/')
def hello_world():
    return render_template('index.html')

@bp.route('/search', methods=['POST'])
def search():
    print(request)
    print(request.form)

    type_ = request.form['type']

    if type_ == "image":
        tmpl = "image_search.html"
        search = image_search
        kw = request.files['logo']
    elif type_ == "text":
        tmpl = "text_search.html"
        search = text_search
        kw = request.form['kw']
    else:
        # abort(404)
        pass

    logos = search(kw)

    return render_template(tmpl, logos=logos)
