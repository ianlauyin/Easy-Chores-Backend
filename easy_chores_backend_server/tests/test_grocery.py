from django.test import TestCase, Client
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.models import Group, User
from ..models.grocery import Grocery
import json


class GroceryTestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.client = Client()
        self.test_group = Group.objects.create(name='Test Group')
        self.user1 = User.objects.create(username='user1')

    def test_grocery_view_post(self):
        new_grocery_data = {
            'user_id': self.user1.id,
            'group_id': self.test_group.id,
            'name': 'Test Grocery',
        }
        response = self.client.post('/grocery', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertIsInstance(response, JsonResponse)
        response_data = json.loads(response.content)
        self.assertTrue('grocery_id' in response_data)
        grocery_id = response_data['grocery_id']

        grocery = Grocery.objects.get(id=grocery_id)
        self.assertEqual(grocery.creator, self.user1)
        self.assertEqual(grocery.group, self.test_group)
        self.assertEqual(grocery.quantity, 1)
        self.assertEqual(grocery.name, 'Test Grocery')

    def test_grocery_view_post_with_quantity(self):
        new_grocery_data = {
            'user_id': self.user1.id,
            'group_id': self.test_group.id,
            'name': 'Test Grocery',
            'quantity': 3
        }
        response = self.client.post('/grocery', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertIsInstance(response, JsonResponse)
        response_data = json.loads(response.content)
        self.assertTrue('grocery_id' in response_data)
        grocery_id = response_data['grocery_id']

        grocery = Grocery.objects.get(id=grocery_id)
        self.assertEqual(grocery.creator, self.user1)
        self.assertEqual(grocery.quantity, 3)
        self.assertEqual(grocery.group, self.test_group)
        self.assertEqual(grocery.name, 'Test Grocery')

    def test_grocery_view_post_with_detail(self):
        new_grocery_data = {
            'user_id': self.user1.id,
            'group_id': self.test_group.id,
            'name': 'Test Grocery',
            'detail': 'Test Detail'
        }
        response = self.client.post('/grocery', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertIsInstance(response, JsonResponse)
        response_data = json.loads(response.content)
        self.assertTrue('grocery_id' in response_data)
        grocery_id = response_data['grocery_id']

        grocery = Grocery.objects.get(id=grocery_id)
        self.assertEqual(grocery.creator, self.user1)
        self.assertEqual(grocery.detail, 'Test Detail')
        self.assertEqual(grocery.group, self.test_group)
        self.assertEqual(grocery.name, 'Test Grocery')

    def test_grocery_view_post_invalid_group(self):
        new_grocery_data = {
            'user_id': self.user1.id,
            'group_id': 0,
            'name': 'Test Grocery',
        }
        response = self.client.post('/grocery', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_grocery_view_post_invalid_user(self):
        new_grocery_data = {
            'user_id': 0,
            'group_id': self.test_group.id,
            'name': 'Test Grocery',
        }
        response = self.client.post('/grocery', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_grocery_view_post_missing_group(self):
        new_grocery_data = {
            'user_id': self.user1.id,
            'name': 'Test Grocery',
        }
        response = self.client.post('/grocery', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_grocery_view_post_missing_user(self):
        new_grocery_data = {
            'group_id': self.test_group.id,
            'name': 'Test Grocery',
        }
        response = self.client.post('/grocery', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
