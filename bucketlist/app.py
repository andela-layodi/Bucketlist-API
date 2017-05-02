import flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource
from flask_login import login_required

# app = flask.Flask(__name__)

from .models import User, BucketList, ListItems


class UserRegistration(Resource):
    """
        /v1/auth/register endpoint
    """

    def post(self):
        """
            Register a user
        """
        pass


class UserLogIn(Resource):
    """
        /v1/auth/login endpoint
    """

    def post(self):
        """
            Log a user in
        """
        pass


class UserLogOut(Resource):
    """
        /v1/auth/logout endpoint
    """

    def post(self):
        """
            Log a user out
        """
        pass


class BucketListNew(Resource):
    """
        /v1/bucketlists/ endpoint
    """

    @login_required
    def post(self):
        """
            Create a new bucketlist
        """
        pass

    @login_required
    def get(self):
        """
            List all the created bucketlists
        """
        pass


class BucketListSingle(Resource):
    """
        /v1/bucketlists/<int:id> endpoint
    """

    @login_required
    def get(self):
        """
            Get single bucketlist
        """
        pass

    @login_required
    def put(self):
        """
            Update single bucketlist
        """
        pass

    @login_required
    def delete(self):
        """
            Delete a single bucketlist
        """
        pass


class BucketListAddItem(Resource):
    """
        /v1/bucketlists/<int:id>/items/ endpoint
    """

    @login_required
    def post(self):
        """
            Create a new item in bucket list
        """
        pass


class BucketListEditItem(Resource):
    """
        /v1/bucketlists/<int:id>/item/<int:id> endpoint
    """

    @login_required
    def put(self):
        """
            Update a bucket list item
        """
        pass

    @login_required
    def delete(self):
        """
            Delete an item in a bucket list
        """
        pass

#
# @app.route('/')
# def hello():
#     return "Hello World!"
#
#
# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run(debug=True)
