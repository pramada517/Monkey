from os.path import abspath, dirname, join
from flask_sqlalchemy import SQLAlchemy

from monkey import app

db = SQLAlchemy(app)

def init_db():
    db.create_all()
