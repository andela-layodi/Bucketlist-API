import unittest
import json

from flask import url_for

from .test_base import InitialTestCase
# from ..bucketlist.models import User, BucketList
# from ..bucketlist.app import db


class BucketListTest(InitialTestCase):

    def test_get_all_bucketlists(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.get(url_for("bucketlists.bucketlist_ops"),
                                   headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_create_new_bucketlist(self):
        new_bucketlist = {
            'list_name': 'Get a tattoo'
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.post(url_for("bucketlists.bucketlist_ops"),
                                    data=json.dumps(new_bucketlist),
                                    headers=headers)
        self.assertEqual(response.status_code, 201)

    # def test_create_existing_bucketlist(self):
    #     new_bucketlist = {
    #         'list_name': 'Get a tattoo'
    #     }
    #     response = self.client.post("/v1/bucketlists/",
    #                                 data=json.dumps(new_bucketlist),
    #                                 content_type='application/json')
    #
    #     self.assertEqual(response.status_code, 201)
    #
    #     response = self.client.post("/v1/bucketlists/",
    #                                 data=json.dumps(new_bucketlist),
    #                                 content_type='application/json')
    #     self.assertEqual(response.status_code, 400)
    #
    # def test_create_bucketlist_with_no_name(self):
    #     new_bucketlist = {}
    #     response = self.client.post("/v1/bucketlists/",
    #                                 data=json.dumps(new_bucketlist),
    #                                 content_type='application/json')
    #     self.assertEqual(response.status_code, 400)
    #
    # def test_list_all_bucketlists(self):
    #     bucketlist = {
    #         'list_name': 'Get a tattoo'
    #     }
    #     response = self.client.get("/v1/bucketlists/",
    #                                data=json.dumps(bucketlist),
    #                                content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_get_single_bucketlist(self):
    #     # bucketlist = {
    #     #     'id': 1,
    #     #     'list_name': 'Get a tattoo'
    #     # }
    #     # x = self.bucketlist
    #     # url = '/v1/bucketlists/{}'.format(x.id)
    #     # response = self.client.get(url,
    #     #                            data=json.dumps(x),
    #     #                            content_type='application/json')
    #     # self.assertEqual(response.status_code, 200)
    #     pass
    #
    # def test_get_wrong_bucketlist(self):
    #     pass
    #
    # def test_update_single_bucketlist(self):
    #     pass
    #
    # def test_delete_single_bucketlist(self):
    #     pass
    #
    # def test_user_unauthenticated(self):
    #     pass


if __name__ == '__main__':
    unittest.run()
