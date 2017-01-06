# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2017-01-04 13:18:25
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-06 19:32:06


from contextlib import closing
import os

import sqlite3

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'logos.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

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
            with open(SCHEMA_PATH, 'r') as f:
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
init_db = db.init


if __name__ == '__main__':
    db.init()
    # db.insert(**{'ind':'2', 'filename':'001.jpg', 'info':'foo', 'theme_colors':'bar', 'ent_name':'alibaba'})
    a = db.query("SELECT * from LOGOS")
    print(len(a))
    # for aa in a:
        # for k, v in aa.items():
            # print(k)
            # print(v)

