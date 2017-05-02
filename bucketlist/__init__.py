import os

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from .config import DevelopmentConfig
from flask_restful import Api

app = Flask(__name__)

# app_settings = os.getenv(
#     'APP_SETTINGS',
#     DevelopmentConfig
# )
app.config.from_object(DevelopmentConfig)

auth_blueprint = Blueprint('auth', __name__)

api = Api(auth_blueprint)
# api = restful.Api(app)

db = SQLAlchemy(app)
