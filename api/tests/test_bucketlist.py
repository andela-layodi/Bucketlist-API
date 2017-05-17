import json
import unittest

from flask import url_for

from .test_base import InitialTestCase


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

    def test_create_existing_bucketlist(self):
        bucketlist = {
            'list_name': 'bucket3'
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }

        response = self.client.post(url_for("bucketlists.bucketlist_ops"),
                                    data=json.dumps(bucketlist),
                                    headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_create_bucketlist_with_no_name(self):
        new_bucketlist = {}
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.post(url_for("bucketlists.bucketlist_ops"),
                                    data=json.dumps(new_bucketlist),
                                    headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_get_single_bucketlist(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.get('/api/v1/bucketlists/1',
                                   headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_update_single_bucketlist(self):
        bucketlist = {
            'list_name': 'Get a tattoo'
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.put('/api/v1/bucketlists/1',
                                   data=json.dumps(bucketlist),
                                   headers=headers)
        self.assertEqual(response.status_code, 202)

    def test_update_single_bucketlist_without_name(self):
        bucketlist = {
            'list_name': ''
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.put('/api/v1/bucketlists/1',
                                   data=json.dumps(bucketlist),
                                   headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_delete_single_bucketlist(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.delete('/api/v1/bucketlists/1',
                                      headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_search_bucketlist(self):
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

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.get('/api/v1/bucketlists?q=bucket',
                                   headers=headers)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.run()
