# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 14:30:16
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-07 11:14:16

import os 

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATASET_DIR = os.path.join(BASE_DIR, 'static', 'dataset')

UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')
ALLOWED_TYPES = {'png', 'jpg', 'jpeg'}

DATABASE_DIR = os.path.join(BASE_DIR, 'database')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'logos.db')
DATABASE_SCHEMA_PATH = os.path.join(DATABASE_DIR, 'schema.sql')
