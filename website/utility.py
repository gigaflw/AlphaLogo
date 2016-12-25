# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 14:02:13
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-25 14:39:56

from config import UPLOAD_DIR, ALLOWED_TYPE

def save_img_to_uploads(im):
    # TODO: type check & size check
    ext = im.filename.split('.')[-1]
    
    if ext not in ALLOWED_TYPE:
        raise TypeError, "Illegal image extension '%s'" % ext

    path = os.path.join(UPLOAD_DIR, 'upload.%s' % ext )
    im.save(path)

    return path
