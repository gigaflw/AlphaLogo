# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-22 20:25:31
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-25 15:22:54

from flask import Blueprint, render_template, abort, request, flash, redirect

from website.core import image_search, text_search

bp = Blueprint('bp', __name__, template_folder='templates')


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/im')
def index_image():
    return render_template('index_image.html')

@bp.route('/search', methods=['POST'])
def search():
    type_ = request.form.get('type')
    kw = None

    if type_ is None:
        flash("parameter 'type' is required in the post data!")

    elif type_ == "image":
        tmpl = "search_image.html"
        search = image_search
        kw = request.files.get('logo')
        print kw

        if kw is None:
            flash("file with name 'logo' is required in the post data. Check your form's enctype.")

    elif type_ == "text":
        tmpl = "search_text.html"
        search = text_search
        kw = request.form.get('kw')

        if kw is None:
            flash("parameter 'kw' is required in the post data!")

    if kw is None:
        logos = []
    else:
        logos = search(kw)

    return render_template(tmpl, logos=logos)
