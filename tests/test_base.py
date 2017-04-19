import unittest

from flask_testing import TestCase
from ..bucketlist.config import TestingConfig

from ..bucketlist.app import app, db


class InitialTestCase(TestCase):

    def create_app(self):
        app.config.from_object(TestingConfig)
        return app

    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.run()
