# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-02 09:41:37
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-04 16:33:44

# 
# To reset index dirs :
#   python manage.py -r
# To move images:
#   python manage.py -m (or you can copy the dir yourself)
# To run pylucene index script :
#   python manage.py -c
# To do the above altogether:
#   python manage.py -i
# 
 
import subprocess
import os
import shutil
import argparse

import cv2

from website.core.index import create_index as core_create_index
from website.core.search_image import create_index as image_create_index
from website.config import DATASET_DIR, ALLOWED_TYPES
from website.core.config import LUCENE_INDEX_DIR, LUCENE_CATELOG_FILE, IMAGE_INDEX_DIR

CRAWL_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crawl')
CRAWL_IMAGE_PATH = os.path.join(CRAWL_BASE, 'pic_jpg')
CRAWL_CATELOG_FILE = os.path.join(CRAWL_BASE, 'PICTURES.txt')


##########################
# Parser define
##########################
parser = argparse.ArgumentParser()
parser.add_argument('-r', action="store_true", help="Reset index dirs")
parser.add_argument('-i', action="store_true", help="Create index files for image search")
parser.add_argument('-c', action="store_true", help="Create index files for non-image search")
parser.add_argument('--init', action="store_true", help="Do everything")

# TODO: not move, but symlink!
##########################
# Functions
##########################
def reset_index():
    dirs = [LUCENE_INDEX_DIR, IMAGE_INDEX_DIR]
    exist_dirs = list(filter(os.path.exists, dirs))

    if exist_dirs:
        r = raw_input("Are you sure to reset '%s'? [y]/n " % "','".join(exist_dirs))
    else:
        r = 'y'

    if r not in ('y', ''):
        return False

    for d in dirs:
        if os.path.exists(d):
            shutil.rmtree(d)
            print("'%s' removed" % d)
        os.mkdir(d)
        print("'%s' created" % d)


    print("Creating symlink '%s' to '%s'..." % (CRAWL_IMAGE_PATH, DATASET_DIR))
    subprocess.call(['ln', '-s', CRAWL_IMAGE_PATH, DATASET_DIR])

    if os.path.isfile(CRAWL_CATELOG_FILE):
        shutil.copyfile(CRAWL_CATELOG_FILE, LUCENE_CATELOG_FILE)
        print("Catelog file '%s' copied to '%s'" % (CRAWL_CATELOG_FILE, LUCENE_CATELOG_FILE))
        return True
    else:
        print("Can't find catelog file '%s'" % CRAWL_CATELOG_FILE)
        return False


def create_index():
    if not reset_index():
        return

    core_create_index()
    image_create_index()


def main():
    args = parser.parse_args()

    if args.r:
        reset_index()
    elif args.c:
        core_create_index()
    elif args.i:
        image_create_index()
    elif args.init:
        create_index()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
