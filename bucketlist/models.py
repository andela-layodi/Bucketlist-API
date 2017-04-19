from werkzeug.security import generate_password_hash, check_password_hash
from bucketlist.app import db


class AddUpdateDelete():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class User(db.Model, AddUpdateDelete):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    bucketlists = db.relationship('BucketList', backref='user', lazy='dynamic')

    def encrypt_password(self, lock):
        self.password = generate_password_hash(
            lock, method='pbkdf2:sha256', salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, first_name, second_name, user_name, email, password):
        self.first_name = first_name
        self.second_name = second_name
        self.user_name = user_name
        self.email = email
        self.password = self.encrypt_password(password)

    def __repr__(self):
        return '<User %r>' % self.user_name


class BucketList(db.Model, AddUpdateDelete):
    __tablename__ = 'buckelists'
    id = db.Column(db.Integer, primary_key=True)
    list_name = db.Column(db.String(100), unique=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    list_items = db.relationship('ListItems', backref='list', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())


class ListItems(db.Model, AddUpdateDelete):
    __tablename__ = 'bucketlistitems'
    id = db.Column(db.Integer, primary_key=True)
    list_title = db.Column(
        db.String(100), db.ForeignKey('buckelists.list_name'))
    item_name = db.Column(db.String(200), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_modified = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
    done = db.Column(db.Boolean, default=False)


def init_db():
    """Initialize the database and create the tables as per the models."""
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    init_db()
