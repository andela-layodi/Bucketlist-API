# import flask
# from flask_sqlalchemy import SQLAlchemy
from bucketlist.app import db

# app = flask.Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bucketlist.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


def init_db():
    """Initialize the database and create the tables as per the models."""
    db.drop_all()
    db.create_all()
