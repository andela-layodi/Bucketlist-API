from flask_login import logout_user
from flask_restful import reqparse, Resource, Api

from api import db
from .models import User
from . import bucketlists

parser = reqparse.RequestParser()
api = Api(bucketlists)


class UserRegistration(Resource):
    """
        /v1/auth/register endpoint
    """

    def post(self):
        """
            Register a user
        """
        parser.add_argument('username')
        parser.add_argument('password')

        args = parser.parse_args()
        username = args['username']
        password = args['password']
        existing_user = db.session.query(User).filter_by(
            username=username).first()
        if username and password:
            if existing_user and existing_user.username == username:
                return {
                    'message': 'This name already exists.'
                    'Choose another username!'}, 400
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return {'message': '{} has been registered into Buckety'
                               .format(username)}, 201
        return {'message': 'Name and passowrd required'}, 400


class UserLogIn(Resource):
    """
        /v1/auth/login endpoint
    """

    def post(self):
        """
            Log a user in
        """
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()
        username = args['username']
        password_hash = args['password']

        user = db.session.query(User).filter_by(username=username).first()
        if password_hash:
            if not user:
                return {'message': "Wrong username."}, 404
            if user.verify_password(password_hash):
                auth_token = user.generate_auth_token(user.id)
                response = {
                    'token': auth_token}, 201
                return response

            return {'message': 'Incorrect password.'}, 400
        return {
            'message': 'Both name and password are required to log in.'}, 400


class UserLogOut(Resource):
    """
        /v1/auth/logout endpoint
    """

    def post(self):
        """
            Log a user out
        """
        logout_user()
        return {'message': 'Logged Out.'}, 200


# endpoints
api.add_resource(
    UserRegistration, '/auth/register', '/auth/register/',
    endpoint="user_registration")
api.add_resource(UserLogIn, '/auth/login', '/auth/login/', endpoint="login")
api.add_resource(UserLogOut, '/auth/logout', endpoint="logout")
