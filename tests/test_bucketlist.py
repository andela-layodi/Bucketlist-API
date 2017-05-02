import unittest
import json

# from werkzeug.security import generate_password_hash

from .test_base import InitialTestCase
# from ..bucketlist.models import User, BucketList
# from ..bucketlist.app import db


class BucketListTest(InitialTestCase):
    # def setUp(self):
    #     self.user_name = user_name
    #     self.password = password
    #     password_hash = generate_password_hash(self.password)
    #     self.user = User(username=self.username, password_hash=password_hash)
    #     db.add(self.user)
    #     db.commit()
    #
    #     # create bucketlist
    #     self.list_name = 'Get a tattoo'
    #     self.bucketlist = BucketList(list_name=self.list_name,
    #                                  creator=self.user.id)
    #     db.add(self.bucketlist)
    #     db.commit()

    def test_create_new_bucketlist(self):
        new_bucketlist = {
            'list_name': 'Get a tattoo'
        }
        response = self.client.post("/v1/bucketlists/",
                                    data=json.dumps(new_bucketlist),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_create_existing_bucketlist(self):
        new_bucketlist = {
            'list_name': 'Get a tattoo'
        }
        response = self.client.post("/v1/bucketlists/",
                                    data=json.dumps(new_bucketlist),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 201)

        response = self.client.post("/v1/bucketlists/",
                                    data=json.dumps(new_bucketlist),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_bucketlist_with_no_name(self):
        new_bucketlist = {}
        response = self.client.post("/v1/bucketlists/",
                                    data=json.dumps(new_bucketlist),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_list_all_bucketlists(self):
        bucketlist = {
            'list_name': 'Get a tattoo'
        }
        response = self.client.get("/v1/bucketlists/",
                                   data=json.dumps(bucketlist),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_single_bucketlist(self):
        # bucketlist = {
        #     'id': 1,
        #     'list_name': 'Get a tattoo'
        # }
        # x = self.bucketlist
        # url = '/v1/bucketlists/{}'.format(x.id)
        # response = self.client.get(url,
        #                            data=json.dumps(x),
        #                            content_type='application/json')
        # self.assertEqual(response.status_code, 200)
        pass

    def test_get_wrong_bucketlist(self):
        pass

    def test_update_single_bucketlist(self):
        pass

    def test_delete_single_bucketlist(self):
        pass

    def test_user_unauthenticated(self):
        pass


if __name__ == '__main__':
    unittest.run()
