import unittest

from flask import current_app as app
from flask_testing import TestCase

from api import create_app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        return create_app('dev')

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://postgres:@localhost/bucketlistdb'
        )


class TestTestingConfig(TestCase):

    def create_app(self):
        return create_app('test')

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql://postgres:@localhost/bucketlistdb_test'
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        return create_app('prod')

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
