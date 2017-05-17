import json
import unittest

from .test_base import InitialTestCase


class ListItemsTest(InitialTestCase):
    def test_create_a_new_list_item(self):
        listitem = {
            'item_name': 'Get a tattoo'
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    data=json.dumps(listitem),
                                    headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_create_a_new_list_item_with_no_name(self):
        listitem = {
            'item_name': ''
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    data=json.dumps(listitem),
                                    headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_get_single_bucketlist_item(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.get('/api/v1/bucketlists/1/items/1/',
                                   headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_update_single_bucketlist_item(self):
        listitem = {
            'item_name': 'Get a tattoo'
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.put('/api/v1/bucketlists/1/items/1/',
                                   data=json.dumps(listitem),
                                   headers=headers)
        self.assertEqual(response.status_code, 202)

    def test_update_single_bucketlist_item_without_name(self):
        listitem = {
            'item_name': ''
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.put('/api/v1/bucketlists/1/items/1/',
                                   data=json.dumps(listitem),
                                   headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_delete_single_bucketlist_item(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.token
        }
        response = self.client.delete('/api/v1/bucketlists/1/items/1/',
                                      headers=headers)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.run()
