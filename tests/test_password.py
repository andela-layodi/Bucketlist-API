import unittest
from ..bucketlist.models import User


class PasswordAuthenticationTest(unittest.TestCase):

    def test_add_password(self):
        encrypt = User(
            username='Layodi',
            email='layodi@layodi.com',
            password='locked123')
        self.assertTrue(encrypt.password is not None)

    def test_password_verified(self):
        locked = User(
            username='Layodi',
            email='layodi@layodi.com',
            password='locked123'
        )
        locked.password('locked123')
        self.assertTrue(locked.verify_password('locked123'))
        self.assertFalse(locked.verify_password('locked1234'))


if __name__ == '__main__':
    unittest.run()
