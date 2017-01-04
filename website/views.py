# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-22 20:25:31
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-01 23:05:26

from flask import Blueprint, render_template, abort, request, flash, redirect, url_for

from website.core import image_search, text_search

bp = Blueprint('bp', __name__, template_folder='templates')


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/im')
def index_image():
    return render_template('index_image.html')


@bp.route('/search', methods=['GET'])
def search():
    """
    Searching by the name of the company or the keywords.
    """
    type_ = request.args.get('type')
    kw = request.args.get('kw')
    ent_name = request.args.get('enterpriseName')
    tmpl = "search.html"
    search_ = text_search

    if len(kw) == 0:
        return redirect(url_for("bp.index"))
    else:
        if type_ == 'search':
            logo_matched, logo_similar = search_(keywords=kw, ent_name='', n_colors='')
        else:
            logo_matched, logo_similar = search_(keywords=kw, ent_name=ent_name, n_colors='')

        # new parameter `n_colors` is added to search function!
        # also `Logo` instance has one more property `theme_colors`
        # It will be required to match `n_colors` goodly to gain a 'good match'!
        # more detail can be seen in the docstring of `core.search.text_search`

    return render_template(tmpl, logo_matched=logo_matched, logo_similar=logo_similar, kw=kw, ent_name=ent_name)

@bp.route('/match', methods=['POST'])
def match():
    """
    Matching the similar pictures by inputting a picture.
    """
    type_ = request.form.get('type')
    kw = None

    if type_ is None:
        flash("parameter 'type' is required in the post data!")

    elif type_ == "match":
        tmpl = "match.html"
        search_ = image_search
        kw = request.files.get('logo')
        print kw

        if kw is None:
            flash("file with name 'logo' is required in the post data. Check your form's enctype.")

    if kw is None:
        logos = []
    else:
        logo_matched, logo_similar = search_(kw)

    return render_template(tmpl, logo_matched=logo_matched, logo_similar=logo_similar, kw=kw)