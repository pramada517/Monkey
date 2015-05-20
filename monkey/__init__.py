from os.path import abspath, dirname, join
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from monkey.database import db

app = Flask(__name__)

def create_app():
    from monkey.model import Monkey
    from monkey.views import *

    _cwd = dirname(abspath(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + join(_cwd, 'monkey.db')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
