import unittest
import json

from flask import url_for

from .test_base import InitialTestCase
from api.bucketlist.models import User
from api import db


class UserAuthenticationTest(InitialTestCase):
    def test_register_user(self):
        new_user = {
            "username": "Layodi",
            "password": "layodi"
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = self.client.post(url_for("bucketlists.user_registration"),
                                    data=json.dumps(new_user),
                                    headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_register_user_with_no_name(self):
        new_user = {
            'password': 'layodi'
        }
        response = self.client.post(url_for("bucketlists.user_registration"),
                                    data=json.dumps(new_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_register_user_with_no_password(self):
        new_user = {
            'user_name': 'layodi'
        }
        response = self.client.post(url_for("bucketlists.user_registration"),
                                    data=json.dumps(new_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        current_user = {
            'username': 'Layodi',
            'password': 'layodi'
        }
        response = self.client.post(url_for("bucketlists.user_registration"),
                                    data=json.dumps(current_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post(url_for("bucketlists.login"),
                                    data=json.dumps(current_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_user_login_with_no_username(self):
        current_user = {
            'username': 'Layodi',
            'password': 'layodi'
        }
        response = self.client.post(url_for("bucketlists.user_registration"),
                                    data=json.dumps(current_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        current_user = {
            'password': 'layodi'
        }
        response = self.client.post(url_for("bucketlists.login"),
                                    data=json.dumps(current_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_user_login_with_no_password(self):
        current_user = {
            'username': 'Layodi',
            'password': 'layodi'
        }
        response = self.client.post(url_for("bucketlists.user_registration"),
                                    data=json.dumps(current_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        current_user = {
            'username': 'layodi'
        }
        response = self.client.post(url_for("bucketlists.login"),
                                    data=json.dumps(current_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_user_login_with_wrong_username(self):
        current_user = {
            'username': 'Layodi',
            'password': 'layodi'
        }
        response = self.client.post(url_for("bucketlists.user_registration"),
                                    data=json.dumps(current_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        current_user = {
            'user_name': 'layodi',
            'password': 'layodi'
        }

        response = self.client.post(url_for("bucketlists.login"),
                                    data=json.dumps(current_user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_generate_auth_token(self):
        user = User(
            username='Layodi',
            password='locked123'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.generate_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))

    def test_verify_auth_token(self):
        user = User(
            username='Layodi',
            password='locked123'
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.generate_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, str))


if __name__ == '__main__':
    unittest.run()
