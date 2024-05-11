from django.test import TestCase, Client
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import Group, User
from django.core.files import File
from django.db.models.query import QuerySet
from ..models.grocery import Grocery
from ..models.grocery_photo import GroceryPhoto
import os
import json


class GroceryPhotoTestCase(TestCase):
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

    def tearDown(self):
        self.remove_photo_file(self.photo1.photo.path)

    def remove_photo_file(self, path):
        if os.path.exists(path):
            os.remove(path)

    def test_grocery_photo_view_post(self):
        with open('./easy_chores_backend_server/tests/test_image2.jpeg', 'rb') as test_photo:
            response = self.client.post(
                f'/groceries/{self.grocery.id}/photos', {'photo': test_photo})
        self.assertIsInstance(response, JsonResponse)
        response_data: dict[str] = json.loads(response.content)
        self.assertTrue('id' in response_data)
        self.assertTrue('url' in response_data)
        self.assertTrue('path' in response_data)
        self.assertTrue(os.path.exists(response_data['path']))
        self.assertTrue(self.grocery.grocery_photos.filter(
            id=response_data['id']).exists())
        self.remove_photo_file(response_data['path'])

    def test_grocery_photo_view_post_invalid_id(self):
        with open('./easy_chores_backend_server/tests/test_image2.jpeg', 'rb') as test_photo:
            response = self.client.post(
                '/groceries/0/photos', {'photo': test_photo})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.grocery.grocery_photos.count(), 1)
        self.assertEqual(GroceryPhoto.objects.count(), 1)

    def test_grocery_photo_view_post_invalid_file(self):
        with open('./easy_chores_backend_server/tests/test_gif.gif', 'rb') as test_photo:
            response = self.client.post(
                f'/groceries/{self.grocery.id}/photos',  {'photo': test_photo})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.grocery.grocery_photos.count(), 1)
        self.assertEqual(GroceryPhoto.objects.count(), 1)

    def test_grocery_photo_views_delete(self):
        response = self.client.delete(f'/groceries/photos/{self.photo1.id}')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.grocery.grocery_photos.count(), 0)
        self.assertFalse(os.path.exists(self.photo1.photo.path))
        self.assertFalse(GroceryPhoto.objects.filter(
            id=self.photo1.id).exists())

    def test_grocery_photo_views_delete_invalid_id(self):
        response = self.client.delete(f'/groceries/photos/0')
        self.assertEqual(response.status_code, 404)
        grocery_photos: QuerySet = self.grocery.grocery_photos.all()
        self.assertIn(self.photo1, grocery_photos)
        self.assertTrue(os.path.exists(self.photo1.photo.path))
