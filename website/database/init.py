# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-11 10:35:19
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-11 22:34:35


from website.database import db
from website.utility import full_path_dataset
from website.core.config import LUCENE_CATELOG_FILE
from website.core.algorithm.utility import get_theme_colors, serialize_colors, serialize_floats
from website.core.algorithm import industry_classify


def create_db():
    print("Reseting sqlite database...")
    db.reset_db()
    db.init()
    
    print("Database inited")

    stat = [0] * 7

    with open(LUCENE_CATELOG_FILE, 'r') as index_f:

        for line in index_f:
            ind, ent_name, info, keywords, imgurl, filename, url = line.split('\t')
            print("adding %s" % ind)

            filename = "{:05d}".format(int(ind)) + '.jpg'

            theme_colors, theme_weights, s, v = get_theme_colors(full_path_dataset(filename))

            theme_colors_for_web = serialize_colors(theme_colors)
            theme_weights = serialize_floats(theme_weights)

            n_colors = str(len(theme_colors))

            indust = industry_classify(info)
            stat[indust] += 1

            to_store = {"ind": ind,
                        "filename": filename,
                        "ent_name": ent_name,
                        "info": info,
                        "theme_colors": theme_colors_for_web,
                        "theme_weights": theme_weights,
                        "s": s,
                        "v": v,
                        "industry": indust
                        }
            db.insert(**to_store)
    print("industry stat", stat)

    print("Sqlite database created.")
