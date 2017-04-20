import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from bucketlist import app, db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bucketlists = db.relationship('BucketList', backref='user', lazy='dynamic')

    def encrypt_password(self, lock):
        self.password = generate_password_hash(
            lock, method='pbkdf2:sha256', salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.encrypt_password(password)
    #
    # def __repr__(self):
    #     return '<User %r>' % self.user_name


class BucketList(db.Model):
    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_name = db.Column(db.String(255), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    list_items = db.relationship('ListItems', backref='list', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    date_modified = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)

    def __init__(self, list_name, created_by, date_created, date_modified):
        self.list_name = list_name
        self.created_by = created_by
        self.date_created = datetime.datetime.now
        self.date_modified = datetime.datetime.now


class ListItems(db.Model):
    __tablename__ = 'bucketlistitems'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_title = db.Column(
        db.String(255), db.ForeignKey('bucketlists.list_name'))
    item_name = db.Column(db.String(255), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
    done = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, list_title, item_name, date_created, date_modified, done=False):
        self.list_title = list_title
        self.item_name = item_name
        self.date_created = datetime.datetime.now
        self.date_modified = datetime.datetime.now
        self.done = done
