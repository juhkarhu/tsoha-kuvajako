from flask_sqlalchemy import SQLAlchemy
from os import getenv
from flask import Flask
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
csrf = CSRFProtect(app)
csrf.init_app(app)

db = SQLAlchemy(app)

from kuvaruutu import routes
