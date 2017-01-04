# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-27 21:45:08
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-04 11:25:27

from __future__ import with_statement, print_function

import os
from time import time
import lucene

from website.core.config import *

# nasty Lucene imports
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
# end


def create_index():
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
    FIELD_PARA = {f: (
        Field.Store.YES if f in STORE_FIELDS else Field.Store.NO,
        Field.Index.ANALYZED if f in INDEX_FIELDS else Field.Index.NO,
    ) for f in ADD_FIELDS}

    for line in indexFile:

        fields = dict(zip(FILE_FIELD_FORMAT, line.split('\t')))

        for f in ADD_FIELDS:
            if f in FIELD_FUNCS:
                fields[f] = FIELD_FUNCS[f](fields)

        print("adding %s" % fields['ind'])

        try:
            doc = Document()

            for f in ADD_FIELDS:
                doc.add(Field(f, fields[f], *FIELD_PARA[f]))

            writer.addDocument(doc)

        except Exception, e:
            print("Failed in indexDocs: %r" % e)
