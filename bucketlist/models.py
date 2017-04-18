from bucketlist.database import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    bucketlists = db.relationship('BucketList')

    def hide_password(self, lock):
        self.password = generate_password_hash(lock)


class BucketList(db.Model):
    __tablename__ = 'buckelists'
    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(50), db.ForeignKey('users.user_name'))
    list_items = db.relationship('ListItems')
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_updated = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())


class ListItems(db.Model):
    __tablename__ = 'bucketlistitems'
    id = db.Column(db.Integer, primary_key=True)
    list_title = db.Column(
        db.String(100), db.ForeignKey('buckelists.list_name'))
    item_name = db.Column(db.String(200), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_updated = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
    achieved = db.Column(db.Boolean, default=False)
