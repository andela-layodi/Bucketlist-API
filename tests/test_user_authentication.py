import unittest
import json
# from werkzeug.security import generate_password_hash

from .test_base import InitialTestCase
# from ..bucketlist.models import User
# from ..bucketlist.app import db


class UserAuthenticationTest(InitialTestCase):
    def test_register_user(self):
        new_user = {
            'user_name': 'layodi',
            'email': 'layodi@layodi.com',
            'password': 'layodi'
        }
        data = json.dumps(new_user)
        print (new_user)
        print (data)
        response = self.client.post("/v1/auth/register",
                                    data=json.dumps(new_user),
                                    content_type='application/json')
        self.assertIn('Successfully registered to Buckety', new_user)
        self.assertEqual(response.status_code, 201)

    def test_register_user_with_no_email(self):
        new_user = {
            'user_name': 'layodi',
            'password': 'layodi'
        }
        response = self.client.post("/v1/auth/register",
                                    data=json.dumps(new_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_register_user_with_no_name(self):
        new_user = {
            'email': 'layodi@layodi.com',
            'password': 'layodi'
        }
        response = self.client.post("/v1/auth/register",
                                    data=json.dumps(new_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_register_user_with_no_password(self):
        new_user = {
            'user_name': 'layodi',
            'email': 'layodi@layodi.com'
        }
        response = self.client.post("/v1/auth/register",
                                    data=json.dumps(new_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        current_user = {
            'user_name': 'layodi',
            'password': 'layodi'
        }
        response = self.client.post('/v1/auth/login',
                                    data=json.dumps(current_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_login_with_no_username(self):
        current_user = {
            'password': 'layodi'
        }
        response = self.client.post('/v1/auth/login',
                                    data=json.dumps(current_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_user_login_with_no_password(self):
        current_user = {
            'user_name': 'layodi'
        }
        response = self.client.post('/v1/auth/login',
                                    data=json.dumps(current_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_user_login_with_wrong_username(self):
        user_name = 'layodi',
        password = 'layodi'

        next_user = {
            'user_name': user_name,
            'password': 'ayodi'
        }

        response = self.client.post('/v1/auth/login',
                                    data=json.dumps(next_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_user_logout(self):
        response = self.client.post('/v1/auth/logout')
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.run()
