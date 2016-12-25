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
BASE_DIR = os.path.join(os.path.dirname(__file__), "index")

# Lucene initialize
vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])

jieba.initialize()

# Standard analyzer
analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)


def _get_lucene_searcher(rel_path):
    path = os.path.join(BASE_DIR, rel_path)
    return IndexSearcher(DirectoryReader.open(SimpleFSDirectory(File(path))))


class SearchConfig:
    index_dir = ''
    searchable_field = "keywords"
    result_keys = ['filename']


def search_func(field, searcher, doc_to_ret_func):
    """Search function factory"""
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

        return list(doc_to_ret_func(keywords, searcher.doc(scoreDoc.doc)) for scoreDoc in scoreDocs)

    return search


def retrieve(keywords, doc):
    return dict(filename=doc.get('filename'))


search = search_func(field=SearchConfig.searchable_field,
                     searcher=_get_lucene_searcher(SearchConfig.index_dir),
                     doc_to_ret_func=retrieve)
