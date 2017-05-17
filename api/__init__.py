from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)

    # Configure version1 blueprint urls
    from api.bucketlist import bucketlists as bucketlists_blueprint
    app.register_blueprint(bucketlists_blueprint,
                           url_prefix='/api/v1')

    return app
