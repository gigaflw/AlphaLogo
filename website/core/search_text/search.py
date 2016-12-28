#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import print_function

import os
import re

import jieba
import lucene

from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher, BooleanClause, BooleanQuery
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.util import Version
from java.io import File

# Index dir name
from website.core.search_text.index import LUCENE_INDEX_DIR

vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])


class SearchConfig:
    result_keys = ['filename', 'ent_name', 'info']
    searchable_field = "keywords"


def get_search_func():
    # Lucene initialize

    jieba.initialize()

    # Standard analyzer
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    searcher = IndexSearcher(DirectoryReader.open(SimpleFSDirectory(File(LUCENE_INDEX_DIR))))

    search = search_func_factory(field=SearchConfig.searchable_field,
                                 analyzer=analyzer,
                                 searcher=searcher)

    return search


def search_func_factory(field, analyzer, searcher):
    """Search function factory"""

    def retrieve(keywords, doc):
        return {k: doc.get(k) for k in SearchConfig.result_keys}

    def search(keywords):
        vm_env.attachCurrentThread()

        keywords = list(filter(lambda x: x, jieba.cut(keywords, cut_all=True)))
        # construct query
        query = BooleanQuery()
        querys = [QueryParser(Version.LUCENE_CURRENT, field, analyzer).parse(kw) for kw in keywords]

        for q in querys:
            query.add(q, BooleanClause.Occur.SHOULD)

        # search
        scoreDocs = searcher.search(query, 50).scoreDocs

        return [retrieve(keywords, searcher.doc(scoreDoc.doc)) for scoreDoc in scoreDocs]

    return search
