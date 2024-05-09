from django.test import TestCase, Client
from django.http import HttpRequest
from django.contrib.auth.models import Group, User
from django.core.files import File
from ..models.grocery import Grocery
from ..models.grocery_photo import GroceryPhoto
import os


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
        with open('./easy_chores_backend_server/tests/test_image2.jpeg', 'rb') as test_photo:
            django_file = File(test_photo)
            self.photo2 = GroceryPhoto.objects.create(
                grocery=self.grocery, photo=django_file)

    def test_grocery_photo_views_delete(self):
        response = self.client.delete(f'/groceries/photos/{self.photo1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.grocery.grocery_photos.count(), 1)
        self.assertFalse(os.path.exists(self.photo1.photo.path))
        self.assertFalse(GroceryPhoto.objects.filter(
            id=self.photo1.id).exists())

    def test_grocery_photo_views_delete_invalid_id(self):
        response = self.client.delete(f'/groceries/photos/0')
        self.assertEqual(response.status_code, 400)
        grocery_photos = self.grocery.grocery_photos.all()
        self.assertIn(self.photo1, grocery_photos)
        self.assertIn(self.photo2, grocery_photos)
        self.assertTrue(os.path.exists(self.photo1.photo.path))
        self.assertTrue(os.path.exists(self.photo1.photo.path))
