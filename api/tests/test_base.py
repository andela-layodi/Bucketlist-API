from flask_testing import TestCase

from api import create_app, db
from api.bucketlist.models import User, BucketList, ListItems


class InitialTestCase(TestCase):
    def create_app(self):
        return create_app('test')

    def setUp(self):
        self.client = self.app.test_client()
        db.create_all()

        # Create a user Mary
        self.user = User("Mary4", "mary")
        db.session.add(self.user)
        db.session.commit()

        self.user = User.query.filter_by(username="Mary4").first()
        self.user.password = "mary"
        self.token = self.user.generate_auth_token(self.user.id)

        # Add bucketlist
        self.bucketlist = BucketList("bucket3", self.user.id)

        db.session.add(self.bucketlist)
        db.session.commit()

        self.bucketlist = BucketList.query.filter_by(
            list_name="bucket3").first()

        # Add bucketlist item
        self.listitem = ListItems(self.bucketlist.id, "listitem2")

        db.session.add(self.listitem)
        db.session.commit()
        self.item = ListItems.query.filter_by(item_name="listitem2").first()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
