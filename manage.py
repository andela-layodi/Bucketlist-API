from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from api import create_app, db
# from api.bucketlist.models import User

app = create_app('dev')
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)

#
# def make_shell_context():
#     return dict(app=app, db=db, User=User)
#
#
# manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


CORS(app)


if __name__ == '__main__':
    manager.run()
    db.create_all()
