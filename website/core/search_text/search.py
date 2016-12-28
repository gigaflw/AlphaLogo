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
    searchable_fields = ['ent_name', 'keywords']


def get_search_func():
    jieba.initialize()

    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    searcher = IndexSearcher(DirectoryReader.open(SimpleFSDirectory(File(LUCENE_INDEX_DIR))))

    search = search_func_factory(analyzer=analyzer,
                                 searcher=searcher)

    return search


def search_func_factory(analyzer, searcher):
    """Search function factory"""

    def retrieve(doc):
        return {k: doc.get(k) for k in SearchConfig.result_keys}

    def search(**kwargs):
        vm_env.attachCurrentThread()
        query = BooleanQuery() 

        for field_name, keywords in kwargs.items():
            # assert field_name in SearchConfig.searchable_fields

            keywords = list(filter(None, jieba.cut(keywords, cut_all=True)))

            # construct query
            for kw in keywords:
                q = QueryParser(Version.LUCENE_CURRENT, field_name, analyzer).parse(kw)
                query.add(q, BooleanClause.Occur.SHOULD)

        # search
        scoreDocs = searcher.search(query, 50).scoreDocs

        return [retrieve(searcher.doc(scoreDoc.doc)) for scoreDoc in scoreDocs]

    return search
