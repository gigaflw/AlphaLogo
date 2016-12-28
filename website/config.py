# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 14:30:16
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-28 15:02:38

import os 

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATASET_DIR = os.path.join(BASE_DIR, 'static', 'dataset')
DATASET_DEMO_DIR = os.path.join(DATASET_DIR, 'demo')

UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_TYPE = {'png', 'jpg', 'jpeg'}
