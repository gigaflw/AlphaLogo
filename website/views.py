# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-22 20:25:31
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-28 21:32:10

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
    tmpl = "search.html"
    search_ = text_search

    if len(kw) == 0:
        return redirect(url_for("bp.index"))
    else:
        logo_matched, logo_similar = search_(keywords=kw, ent_name='')

    return render_template(tmpl, logo_matched=logo_matched, logo_similar=logo_similar, kw=kw)

@bp.route('/senior_search', methods=['POST'])
def senior_search():
    """
    Senior search. Searching by the keywords.
    """
    type_ = request.form.get('type')
    kw = None

    tmpl = "senior_search.html"
    search_ = text_search
    kw = request.form.get('kw')

    if kw is None:
        logos = []
    else:
        logos = search_(kw)

    logo_matched = logos[:1] # fake data
    logo_similar = logos[1:] # fake data

    return render_template(tmpl, logo_matched=logo_matched, logo_similar=logo_similar, webtype=type_, kw=kw)

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
        logos = search_(kw)

    logo_matched = logos[:1] # fake data
    logo_similar = logos[1:] # fake data

    return render_template(tmpl, logo_matched=logo_matched, logo_similar=logo_similar, kw=kw)