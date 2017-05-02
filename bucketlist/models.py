import datetime
import jwt

from werkzeug.security import generate_password_hash, check_password_hash

from . import app, db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def verify_auth_token(self, auth_token):
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

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username


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

    def to_json(self):
        return {
            "id": self.id,
            "name": self.list_name,
            "items": [{item.to_json} for item in self.list_items],
            "date_created": str(self.date_created),
            "date_modified": str(self.date_modified),
            "created_by": self.created_by
        }

    def __repr__(self):
        return '<BucketList %r>' % self.list_name


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

    def __init__(
            self, list_title, item_name, date_created, date_modified, done=False):
        self.list_title = list_title
        self.item_name = item_name
        self.date_created = datetime.datetime.now
        self.date_modified = datetime.datetime.now
        self.done = done

    def to_json(self):
        return {
            "id": self.id,
            "name": self.item_name,
            "date_created": str(self.date_created),
            "date_modified": str(self.date_modified),
            "done": self.done
        }

    def __repr__(self):
        return '<ListItems %r>' % self.item_name
