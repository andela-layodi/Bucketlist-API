from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from bucketlist import app, db, api
from bucketlist.bucketlist_resources import BucketListNew, BucketListAddItem, BucketListSingle, BucketListEditItem
from bucketlist.models import User
from bucketlist.user_authentication import UserRegistration, UserLogIn, UserLogOut

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


# endpoints
api.add_resource(
    UserRegistration, '/api/v1/auth/register', endpoint="user_registration")
api.add_resource(UserLogIn, '/api/v1/auth/login', endpoint="login")
api.add_resource(UserLogOut, '/api/v1/auth/logout', endpoint="logout")
api.add_resource(
    BucketListNew, '/api/v1/bucketlists/', endpoint="newbucketlist")
api.add_resource(BucketListAddItem, '/api/v1/bucketlists/<int:id>/items/',
                 endpoint='add_bucketlistitems')
api.add_resource(
    BucketListSingle, '/api/v1/bucketlists/<int:id>',
    '/api/v1/bucketlists/<int:id>/',
    endpoint='single_bucketlist')
api.add_resource(
    BucketListEditItem, '/api/v1/bucketlists/<int:id>/items/<item_id>/',
    endpoint='update_item')

CORS(app)


if __name__ == '__main__':
    manager.run()
