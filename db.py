from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import os

app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')

db = SQLAlchemy(app)

# def db_init(app):
#     db.init_app(app)

#     # Creates the logs tables if the db doesnt already exist
#     with app.app_context():
#         db.create_all()