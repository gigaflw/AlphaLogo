# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-04 13:18:25
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-12 20:59:30
# 
# A wrap around sqlite3 refers to 'http://dormousehole.readthedocs.io/en/latest/patterns/sqlite3.html'
# 

from contextlib import closing

import sqlite3

from website.config import DATABASE_PATH, DATABASE_SCHEMA_PATH

class DB(object):
    def init(self):
        if not hasattr(self, '_db'):
            setattr(self, '_db', self._connect_db())
        
    def query(self, query, args=(), one=False):
        cur = self._db.execute(query, args)
        rv = [dict((cur.description[idx][0].lower(), value)
                   for idx, value in enumerate(row)) for row in cur.fetchall()]
        return (rv[0] if rv else None) if one else rv

    def insert(self, **kwargs):
        k,v = zip(*kwargs.items())
        k = ', '.join(k)
        v = [vv.decode('utf-8') if isinstance(vv, str) else vv for vv in v]
        cmd = "INSERT INTO LOGOS (%s) VALUES (%s)" % (k, ','.join(['?'] * len(kwargs)))
        self._db.execute(cmd, v)
        self._db.commit()

    @classmethod
    def reset_db(cls):
        with closing(cls._connect_db()) as db:
            with open(DATABASE_SCHEMA_PATH, 'r') as f:
                db.cursor().executescript(f.read())
            db.commit()

    @staticmethod
    def _connect_db():
        return sqlite3.connect(DATABASE_PATH)

    def connect(self):
        self._db = self._connect_db()

    def close(self):
        self._db.close()

db = DB()


