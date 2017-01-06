# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 14:02:13
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-06 14:35:35

import os, shutil
from time import ctime
from hashlib import md5

from config import UPLOAD_DIR, DATASET_DIR, ALLOWED_TYPES


def save_img_to_uploads(im, clear_others_if_more_than=10):
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
    return os.path.join([DATASET_DIR, name])
