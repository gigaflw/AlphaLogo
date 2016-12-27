# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-27 21:45:08
# @Last Modified by:   GigaFlower
# @Last Modified time: 2016-12-27 22:44:16

from __future__ import with_statement

import sys
import os
import lucene
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version


class IndexFiles(object):

    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, storeDir, indexFile, analyzer):
        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(indexFile, writer)
        print 'commit index',
        writer.commit()
        writer.close()
        print 'done'

    def indexDocs(self, indexFile, writer):
        for line in indexFile:

            ind, name, info, kw, _ = line.split('\t')
            kw = ' '.join(kw.split('%'))
            filename = "{:05d}".format(int(ind)) + '.jpg'

            print "adding", ind

            try:
                doc = Document()
                doc.add(Field("filename", filename, Field.Store.YES, Field.Index.NO))
                doc.add(Field("ent_name", name, Field.Store.YES, Field.Index.NO))
                doc.add(Field("info", info, Field.Store.YES, Field.Index.NO))
                doc.add(Field("keywords", kw, Field.Store.NO, Field.Index.ANALYZED))

                writer.addDocument(doc)
            except Exception, e:
                print "Failed in indexDocs:", e



if __name__ == '__main__':
    INDEX_DIR = "web.index"
    BASE_DIR = os.path.dirname(__file__)
    STORE_DIR = os.path.join(BASE_DIR, INDEX_DIR)

    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()

    with open(os.path.join(BASE_DIR, 'PICTURES.txt'), 'r') as index_f:
        IndexFiles(storeDir=STORE_DIR,
                   indexFile=index_f,
                   analyzer=StandardAnalyzer(Version.LUCENE_CURRENT))
    end = datetime.now()
    print end - start
