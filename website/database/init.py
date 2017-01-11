# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-11 10:35:19
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-11 12:55:45


from website.database import db
from website.utility import full_path_dataset
from website.core.config import LUCENE_CATELOG_FILE
from website.core.algorithm.utility import get_theme_colors, serialize_colors, serialize_floats


def create_db(do_image_pickle):
    print("Reseting sqlite database...")
    db.reset_db()
    db.init()
    
    print("Database inited")

    with open(LUCENE_CATELOG_FILE, 'r') as index_f:

        for line in index_f:
            ind, ent_name, info, keywords, imgurl, filename, url = line.split('\t')
            print("adding %s" % ind)

            filename = "{:05d}".format(int(ind)) + '.jpg'

            theme_colors, theme_weights, s, v = get_theme_colors(full_path_dataset(filename))

            theme_colors_for_web = serialize_colors(theme_colors)
            theme_weights = serialize_floats(theme_colors)

            n_colors = str(len(theme_colors))

            
            to_store = {"ind": ind,
                        "filename": filename,
                        "ent_name": ent_name,
                        "info": info,
                        "theme_colors": theme_colors_for_web,
                        "theme_weights": theme_weights,
                        "s": s,
                        "v": v
                        }
            db.insert(**to_store)

    print("Sqlite database created.")
