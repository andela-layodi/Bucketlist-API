from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from .config import DevelopmentConfig

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

api = Api(app)

db = SQLAlchemy(app)
