# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-27 21:45:08
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-14 13:42:14

from __future__ import with_statement, print_function

from time import time
import lucene
import jieba

# nasty Lucene imports
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
# from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import SimpleAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
# end

from website.core.config import LUCENE_CATELOG_FILE, LUCENE_INDEX_DIR


def create_index():

    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print('lucene %s is working ...' % lucene.VERSION)

    start = time()
    with open(LUCENE_CATELOG_FILE, 'r') as index_f:
        _index_files(storeDir=LUCENE_INDEX_DIR, indexFile=index_f)
    end = time()

    print("time consumed: %.5f" % (end - start))


def _index_files(storeDir, indexFile):
    jieba.initialize()

    store = SimpleFSDirectory(File(storeDir))
    analyzer = SimpleAnalyzer(Version.LUCENE_CURRENT)
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

        ind, ent_name, info, keywords, imgurl, filename, url = line.split('\t')
        print("adding %s" % ind)

        filename = "{:05d}".format(int(ind)) + '.jpg'
        keywords = keywords.replace('%', ' ')

        ent_name = " ".join(x.strip() for x in jieba.cut_for_search(ent_name))
        keywords = " ".join(x.strip() for x in jieba.cut_for_search(keywords))

        try:
            doc = Document()

            doc.add(Field('ind', ind, Field.Store.YES, Field.Index.NO))
            doc.add(Field('ent_name', ent_name, Field.Store.NO, Field.Index.ANALYZED))
            doc.add(Field('keywords', keywords, Field.Store.NO, Field.Index.ANALYZED))
            # doc.add(Field('n_colors', n_colors, Field.Store.NO, Field.Index.ANALYZED))

            writer.addDocument(doc)

        except Exception, e:
            print("Failed in indexDocs: %r" % e)
