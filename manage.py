# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-02 09:41:37
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-02 12:18:11

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
from website.config import DATASET_DIR, ALLOWED_TYPES
from website.core.config import IMAGE_MIRROR_DIR, LUCENE_INDEX_DIR, LUCENE_CATELOG_FILE

CRAWL_IMAGE_PATH = os.path.join('crawl', 'pic_jpg')
CRAWL_CATELOG_FILE = os.path.join('crawl', 'PICTURES.txt')


##########################
# Parser define
##########################
parser = argparse.ArgumentParser()
parser.add_argument('-r', action="store_true", help="Reset index dirs")
parser.add_argument('-m', action="store_true", help="Move images")
parser.add_argument('-c', action="store_true", help="Create index")
parser.add_argument('-i', action="store_true", help=" = -rmc")


##########################
# Functions
##########################
def reset_index():
    dirs = [DATASET_DIR, LUCENE_INDEX_DIR]
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

    os.remove(IMAGE_MIRROR_DIR)
    os.symlink(DATASET_DIR, IMAGE_MIRROR_DIR)  # FIXME: can windows use this?
    print("Image soft link '%s' has been created" % IMAGE_MIRROR_DIR)

    return True


def move_images():
    for file_name in os.listdir(CRAWL_IMAGE_PATH):
        new_file_name, ext = file_name.rsplit('.', 1)
        new_file_name = "%s.jpg" % new_file_name

        if ext in ALLOWED_TYPES:
            im = cv2.imread(os.path.join(CRAWL_IMAGE_PATH, file_name))
            cv2.imwrite(os.path.join(DATASET_DIR, new_file_name), im)
            print("Moved '%s'" % new_file_name)
        else:
            print("Illegal image type '%s' ignored" % file_name)

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

    if not move_images():
        return

    core_create_index()


def main():
    args = parser.parse_args()

    if args.r:
        reset_index()
    elif args.m:
        move_images()
    elif args.c:
        core_create_index()
    elif args.i:
        create_index()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
