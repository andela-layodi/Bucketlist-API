"""
    This file defines the serializing method to
    be used by the marshal function.
"""

from flask_restful import fields

bucketlistitems = {
    'id': fields.Integer,
    'item_name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.Boolean
}

bucketlists = {
    'id': fields.Integer,
    'list_name': fields.String,
    'created_by': fields.String,
    'list_items': fields.Nested(bucketlistitems),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}
