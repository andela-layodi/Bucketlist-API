import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'bucketlist.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

db = SQLAlchemy(app)
