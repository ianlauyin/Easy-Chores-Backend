from django.test import TestCase, Client
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.models import Group, User
from django.forms.models import model_to_dict
from django.core.files import File
from ..models.grocery import Grocery
from ..models.grocery_photo import GroceryPhoto
import json
import os


class GroceryTestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.client = Client()
        self.test_group = Group.objects.create(name='Test Group')
        self.user1 = User.objects.create(username='user1')
        self.grocery = Grocery.objects.create(
            creator=self.user1, group=self.test_group, name='Test Grocery')
        with open('./easy_chores_backend_server/tests/test_image.png', 'rb') as test_photo:
            django_file = File(test_photo)
            self.photo1 = GroceryPhoto.objects.create(
                grocery=self.grocery, photo=django_file)
        with open('./easy_chores_backend_server/tests/test_image2.jpeg', 'rb') as test_photo:
            django_file = File(test_photo)
            self.photo2 = GroceryPhoto.objects.create(
                grocery=self.grocery, photo=django_file)

    def tearDown(self):
        if os.path.exists(self.photo1.photo.path):
            os.remove(self.photo1.photo.path)
        if os.path.exists(self.photo2.photo.path):
            os.remove(self.photo2.photo.path)

    def test_grocery_view_get(self):
        response = self.client.get(f'/groceries/{self.grocery.id}')
        self.assertIsInstance(response, JsonResponse)
        response_data = json.loads(response.content)
        self.assertDictEqual(
            response_data['grocery'], model_to_dict(self.grocery))
        self.assertIn(self.photo1.photo.url, response_data['photos'])
        self.assertIn(self.photo2.photo.url, response_data['photos'])

    def test_grocery_view_get_without_photos(self):
        new_grocery = Grocery.objects.create(
            creator=self.user1, group=self.test_group, name='New Test Grocery')
        response = self.client.get(f'/groceries/{new_grocery.id}')
        self.assertIsInstance(response, JsonResponse)
        response_data = json.loads(response.content)
        self.assertDictEqual(
            response_data['grocery'], model_to_dict(new_grocery))
        self.assertListEqual(response_data['photos'], [])

    def test_grocery_view_get_invalid_id(self):
        response = self.client.get(f'/groceries/0')
        self.assertEqual(response.status_code, 400)

    def test_grocery_view_post(self):
        new_grocery_data = {
            'user_id': self.user1.id,
            'group_id': self.test_group.id,
            'name': 'New Test Grocery',
        }
        response = self.client.post(
            '/groceries',
            json.dumps(new_grocery_data),
            content_type='application/json',
        )
        self.assertIsInstance(response, JsonResponse)
        response_data = json.loads(response.content)
        self.assertTrue('grocery_id' in response_data)
        grocery_id = response_data['grocery_id']

        grocery = Grocery.objects.get(id=grocery_id)
        self.assertEqual(grocery.creator, self.user1)
        self.assertEqual(grocery.group, self.test_group)
        self.assertEqual(grocery.quantity, 1)
        self.assertEqual(grocery.name, 'New Test Grocery')

    def test_grocery_view_post_with_quantity(self):
        new_grocery_data = {
            'user_id': self.user1.id,
            'group_id': self.test_group.id,
            'name': 'New Test Grocery',
            'quantity': 3
        }
        response = self.client.post('/groceries', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertIsInstance(response, JsonResponse)
        response_data = json.loads(response.content)
        self.assertTrue('grocery_id' in response_data)
        grocery_id = response_data['grocery_id']

        grocery = Grocery.objects.get(id=grocery_id)
        self.assertEqual(grocery.creator, self.user1)
        self.assertEqual(grocery.quantity, 3)
        self.assertEqual(grocery.group, self.test_group)
        self.assertEqual(grocery.name, 'New Test Grocery')

    def test_grocery_view_post_with_detail(self):
        new_grocery_data = {
            'user_id': self.user1.id,
            'group_id': self.test_group.id,
            'name': 'New Test Grocery',
            'detail': 'New Test Detail'
        }
        response = self.client.post('/groceries', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertIsInstance(response, JsonResponse)
        response_data = json.loads(response.content)
        self.assertTrue('grocery_id' in response_data)
        grocery_id = response_data['grocery_id']

        grocery = Grocery.objects.get(id=grocery_id)
        self.assertEqual(grocery.creator, self.user1)
        self.assertEqual(grocery.detail, 'New Test Detail')
        self.assertEqual(grocery.group, self.test_group)
        self.assertEqual(grocery.name, 'New Test Grocery')

    def test_grocery_view_post_invalid_group(self):
        new_grocery_data = {
            'user_id': self.user1.id,
            'group_id': 0,
            'name': 'New Test Grocery',
        }
        response = self.client.post('/groceries', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_grocery_view_post_invalid_user(self):
        new_grocery_data = {
            'user_id': 0,
            'group_id': self.test_group.id,
            'name': 'New Test Grocery',
        }
        response = self.client.post('/groceries', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_grocery_view_post_missing_group(self):
        new_grocery_data = {
            'user_id': self.user1.id,
            'name': 'New Test Grocery',
        }
        response = self.client.post('/groceries', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_grocery_view_post_missing_user(self):
        new_grocery_data = {
            'group_id': self.test_group.id,
            'name': 'New Test Grocery',
        }
        response = self.client.post('/groceries', json.dumps(new_grocery_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_grocery_view_put(self):
        update_data = {
            'name': "Updated Test Grocery",
            "detail": "Updated Test Detail",
            "quantity": 5
        }
        response = self.client.put(
            f'/groceries/{self.grocery.id}', json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.grocery.refresh_from_db()
        self.assertEqual(self.grocery.name, 'Updated Test Grocery')
        self.assertEqual(self.grocery.detail, 'Updated Test Detail')
        self.assertEqual(self.grocery.quantity, 5)

    def test_grocery_view_put_only_name(self):
        update_data = {
            'name': "Updated Test Grocery",
        }
        response = self.client.put(
            f'/groceries/{self.grocery.id}', json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.grocery.refresh_from_db()
        self.assertEqual(self.grocery.name, 'Updated Test Grocery')
        self.assertEqual(self.grocery.detail, '')
        self.assertEqual(self.grocery.quantity, 1)

    def test_grocery_view_put_wrong_key(self):
        update_data = {
            "test": "test"
        }
        response = self.client.put(
            f'/groceries/{self.grocery.id}', json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_grocery_view_put_invalid_id(self):
        update_data = {
            'name': "Updated Test Grocery",
            "detail": "Updated Test Detail",
            "quantity": 5
        }
        response = self.client.put(
            f'/groceries/0', json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_grocery_view_delete(self):
        response = self.client.delete(f'/groceries/{self.grocery.id}')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(GroceryPhoto.objects.filter(
            id=self.photo1.id).exists())
        self.assertFalse(GroceryPhoto.objects.filter(
            id=self.photo2.id).exists())
        self.assertFalse(os.path.exists(self.photo1.photo.path))
        self.assertFalse(os.path.exists(self.photo2.photo.path))
        self.assertFalse(Grocery.objects.filter(id=self.grocery.id).exists())

    def test_grocery_view_delete_invalid_id(self):
        response = self.client.delete(f'/groceries/0')
        self.assertEqual(response.status_code, 400)
