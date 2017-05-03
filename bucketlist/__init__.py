import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import DevelopmentConfig
from flask_restful import Api

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

api = Api(app)

db = SQLAlchemy(app)
