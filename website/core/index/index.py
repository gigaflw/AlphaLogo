# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-27 21:45:08
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-06 21:39:06

from __future__ import with_statement, print_function

import os
from time import time
import lucene
from flask import g

from website.database import db
from website.utility import full_path_dataset
from website.core.config import *
from website.core.index.utility import get_theme_colors, to_web_color

# nasty Lucene imports
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
# end


FILE_FIELD_FORMAT = ["ind", "ent_name", "info", "keywords", "imgurl", "filename", "url"]
STORE_FIELDS = ["ind", "filename", "ent_name", "info", "theme_colors", "style_tag"]  # values saved to sqlite db
PRIMARY_KEY = 'ind'  # value stored in lucene
INDEX_FIELDS = ["ent_name", "keywords", "n_colors"]  # value indexed in lucene
ADD_FIELDS = STORE_FIELDS + INDEX_FIELDS

ADD_FIELDS.insert(4, '_theme_colors')

FIELD_FUNCS = {
    "filename": lambda f: "{:05d}".format(int(f['ind'])) + '.jpg',
    "keywords": lambda f: f['keywords'].replace('%', ' '),
    "_theme_colors": lambda f: theme_colors(f['filename']),
    "theme_colors": lambda f: " ".join(map(to_web_color, f['_theme_colors'])),
    "n_colors": lambda f: str(len(f['_theme_colors'])),
    "style_tag": lambda f: color_style_tag(f['filename']),
}


def create_index():
    db.reset_db()
    db.init()

    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene %s is working ...' % lucene.VERSION)

    start = time()
    with open(LUCENE_CATELOG_FILE, 'r') as index_f:
        _index_files(storeDir=LUCENE_INDEX_DIR, indexFile=index_f)
    end = time()

    print("time consumed: %.5f" % (end - start))


def _index_files(storeDir, indexFile):
    store = SimpleFSDirectory(File(storeDir))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)

    config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)

    writer = IndexWriter(store, config)

    _index_docs(indexFile, writer)

    print('commit index')
    writer.commit()
    writer.close()
    print('done')


def _index_docs(indexFile, writer):
    for line in indexFile:

        # fields = dict(zip(FILE_FIELD_FORMAT, line.split('\t')))

        # for f in ADD_FIELDS:
        #     if f in FIELD_FUNCS:
        #         fields[f] = FIELD_FUNCS[f](fields)

        ind, ent_name, info, keywords, imgurl, filename, url = line.split('\t')
        print("adding %s" % ind)

        filename = "{:05d}".format(int(ind)) + '.jpg'
        keywords = keywords.replace('%', ' ')

        theme_colors, style_tag = get_theme_colors(full_path_dataset(filename))
        
        # stat[style_tag] += 1
        
        theme_colors_for_web = " ".join(map(to_web_color, theme_colors))

        n_colors = str(len(theme_colors))

        #########################
        # pylucene insertion
        #########################
        STORE_FIELDS = ["ind", "filename", "ent_name", "info", "theme_colors", "style_tag"]  # values saved to sqlite db
        INDEX_FIELDS = ["ent_name", "keywords", "n_colors"]  # value indexed in lucene

        try:
            doc = Document()

            # for f in INDEX_FIELDS:
            #     doc.add(Field(f, fields[f], Field.Store.NO, Field.Index.ANALYZED))

            doc.add(Field('ind', ind, Field.Store.YES, Field.Index.NO))
            doc.add(Field('ent_name', ent_name, Field.Store.NO, Field.Index.ANALYZED))
            doc.add(Field('keywords', keywords, Field.Store.NO, Field.Index.ANALYZED))
            doc.add(Field('n_colors', n_colors, Field.Store.NO, Field.Index.ANALYZED))

            writer.addDocument(doc)

        except Exception, e:
            print("Failed in indexDocs: %r" % e)

        ##########################
        # sqlite insertion
        ##########################
        # to_store = {k: fields[k] for k in STORE_FIELDS}
        to_store = {"ind": ind,
                    "filename": filename,
                    "ent_name": ent_name,
                    "info": info, 
                    "theme_colors": theme_colors_for_web,
                    "style_tag": style_tag
                    }
        db.insert(**to_store)
