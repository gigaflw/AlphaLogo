# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 13:07:33
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-27 18:53:20

try:
    import cPickle as pickle
except ImportError:
    import pickle

import numpy as np
import cv2

from website.config import DATASET_DEMO_DIR


def pre_compute():
    """
    Compute the descriptors of images in datasets ahead of time
    """
    pass

def save_data(data):
    """
    Save the precompute data into pickle file
    """
    pass

def load_data():
    """
    Load the precomputed data
    """
    pass

def search(path):
    """
    logo matching function
    
    @param: path: the path to the target logo image file
    @return: a list of indexes, sorted in the order of similarity
    """
    return []