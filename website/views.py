# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-22 20:25:31
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-07 11:45:40

from flask import Blueprint, render_template, abort, request, flash, redirect, url_for

from website.core import image_search, text_search
from website.utility import save_img_to_uploads, full_path_uploads


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
    n_colors = request.args.get('nColors')
    saturation = request.args.get('saturation')
    value = request.args.get('brightness')
    tmpl = "search.html"
    search_ = text_search

    print n_colors
    print saturation
    print value

    n_color_list = data_convertion(n_colors, 1)
    saturation_list = data_convertion(saturation)
    value_list = data_convertion(value)

    print n_color_list
    print saturation_list
    print value_list

    if len(kw) == 0:
        return redirect(url_for("bp.index"))
    else:
        if type_ == 'search':
            logo_matched = search_(keywords=kw, ent_name='', n_colors=[])
        else:
            logo_matched = search_(keywords=kw, ent_name=ent_name, n_colors=n_color_list, saturation_level=saturation_list, value_level=value_list)

        # new parameter `n_colors` is added to search function!
        # also `Logo` instance has one more property `theme_colors`
        # It will be required to match `n_colors` goodly to gain a 'good match'!
        # more detail can be seen in the docstring of `core.search.text_search`

    return render_template(tmpl, logo_matched=logo_matched, logo_similar=[], kw=kw, ent_name=ent_name, n_colors=n_colors)


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

        if not kw.filename:
            return redirect(url_for("bp.index"))
            flash("file with name 'logo' is required in the post data. Check your post data.")
            upload_name = ""
        else:
            upload_name = save_img_to_uploads(kw, clear_others_if_more_than=10)
            ##########################
            # Delete after reading
            ##########################
            # TODO: Hu:
            # upload_name is the filename of the uploaded file, no directory names included
            # will passed to your template with the name 'upload'
            # When there are more than 10 picutrues in the upload dir, all images will deleted automatically
            # this behavior can be modified by the parameter `clear_others_if_more_than`
            # usage:
            # <img src="/static/uploads/{{ upload }}">

    if kw is None:
        return redirect(url_for("bp.index"))
    else:
        logo_matched, logo_similar = search_(full_path_uploads(upload_name))

    return render_template(tmpl, logo_matched=logo_matched, logo_similar=logo_similar, kw=kw, upload=upload_name)

def data_convertion(data, mode=0):
    # mode=0 means normal mode excluding color input; mode=1 means color input.
    data_list = []
    data_split = data.split(",")
    if (mode == 0):
        for i in range(len(data_split)):
            if (data_split[i] == u"1"):
                data_list.append(i)
    elif (mode == 1):
        for i in range(len(data_split)):
            if (data_split[i] == u"1"):
                if (i == len(data_split)-1):
                    data_list.append(0)
                else:
                    data_list.append(i+2)
    return data_list