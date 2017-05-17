from flask import Blueprint

bucketlists = Blueprint('bucketlists', __name__)
# Import last to prevent Import Error

from . import bucketlist_resources, user_authentication
