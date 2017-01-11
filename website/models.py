# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-25 12:18:32
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-11 22:38:21


from collections import namedtuple

Logo = namedtuple('Logo', ['ind', 'filename', 'ent_name', 'info', 'theme_colors', 'theme_weights', 's', 'v', 'industry'])

# ind: a string denoting the index
# filename: relative path to 'dataset'
# ent_name: string, denoting the name of the brand
# info: a paragraph describing the logo
# theme_color: a list of web color, e.g. ['#ff0abc', ...]
# theme_weights: a list of floats denoting the proportion of theme colors, ranged (0, 1)
# s: a float, the average value of 's' in hsv
# v: a float, the average value of 'v' in hsv
# industry: a int constant denoting the industry this logo envolved with, defined in `core.algorithm.industry_classify`
# 
