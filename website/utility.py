# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 14:02:13
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-12 20:56:30

import os
import shutil
from time import ctime
from hashlib import md5

from config import UPLOAD_DIR, DATASET_DIR, ALLOWED_TYPES


def save_img_to_uploads(im, clear_others_if_more_than=10):
    """
    Save imgs to upload dir, which also
    1) clean the dir if there are more than `clear_others_if_more_than` imgs
    2) check the image extension
    3) hash file name to avoid cache

    @param: im: the image binary data get from flask uploads
    @return: the hashed filename of the uploaded file
    """
    if clear_others_if_more_than and len(os.listdir(UPLOAD_DIR)) > clear_others_if_more_than:
        shutil.rmtree(UPLOAD_DIR)
        os.mkdir(UPLOAD_DIR)
        print("Upload dir '%s' cleaned" % UPLOAD_DIR)

    # TODO: type check & size check
    ext = im.filename.split('.')[-1]

    if ext not in ALLOWED_TYPES:
        raise TypeError, "Illegal image extension '%s'" % ext

    name = md5(ctime().encode()).hexdigest()
    filename = "%s.%s" % (name, ext)
    path = os.path.join(UPLOAD_DIR, filename)
    im.save(path)

    return filename


def full_path_uploads(name):
    ret = os.path.join(UPLOAD_DIR, name)
    return ret


def full_path_dataset(name):
    return os.path.join(DATASET_DIR, name)


# delayed import to avoid cyclic import
from website.models import Logo
from website.core.algorithm.utility import get_theme_colors, to_web_color


def get_uploaded_logo(name):    
    theme_colors, theme_weights, s, v = get_theme_colors(full_path_uploads(name))
    theme_colors_for_web = list(map(to_web_color, theme_colors))
    theme_weights = list(theme_weights)

    return Logo(ind=-1, filename=name, ent_name='', info='',
                theme_colors=theme_colors_for_web, theme_weights=theme_weights,
                s=s, v=v, industry=-1)
