import datetime

import jwt
from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from api import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    bucketlists = db.relationship('BucketList', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot view this')

    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(
            pwd, method='pbkdf2:sha256', salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, user_id):
        """
        Generates the Auth Token
        """
        try:
            payload = {
                # expiration data of token
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=0, seconds=3600),
                # time token was generated
                'iat': datetime.datetime.utcnow(),
                # user that is identified by the token
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            ).decode()
        except Exception as e:
            return e

    @staticmethod
    def verify_auth_token(auth_token):
        """
        Verifies the auth token
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


class BucketList(db.Model):
    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_name = db.Column(db.String(255), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    list_items = db.relationship(
        'ListItems', backref="set", cascade="all", lazy="joined")
    date_created = db.Column(
        db.DateTime, default=db.func.now(), nullable=False)
    date_modified = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(),
        nullable=False)

    def __init__(self, list_name, created_by):
        self.list_name = list_name
        self.created_by = created_by

    def __repr__(self):
        return '<BucketList %r>' % self.list_name


class ListItems(db.Model):
    __tablename__ = 'bucketlistitems'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    item_name = db.Column(db.String(255), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
    done = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(
            self, list_id, item_name):
        self.list_id = list_id
        self.item_name = item_name

    def __repr__(self):
        return '<ListItems %r>' % self.item_name
