# -*- coding: utf-8 -*-
# @Author: GigaFlower
# @Date:   2016-12-22 20:23:50
# @Last Modified by:   GigaFlower
# @Last Modified time: 2017-01-04 15:15:16

from flask import Flask

from website.views import bp
from website.database import init_db, db
from website.core import init_searcher

def create_app():
    app = Flask(__name__)
    app.secret_key = "God_is_dog"
    init_db()
    init_searcher()

    @app.before_request
    def before_request():
        db.connect()

    @app.teardown_request
    def teardown_request(exception):
        db.close()
        
    app.register_blueprint(bp)
    return app
