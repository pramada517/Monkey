from os.path import abspath, dirname, join
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
_cwd = dirname(abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + join(_cwd, 'monkey.db')

from monkey.model import Monkey
from monkey.views import *


