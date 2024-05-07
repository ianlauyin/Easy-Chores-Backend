from django.test import TestCase, Client
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.models import Group, User
from ..views.group_user_views import GroupUserViews
import json


class GroupUserTestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.client = Client()
        self.group_user_view = GroupUserViews()
        self.test_group = Group.objects.create(name='Test Group')
        self.user1 = User.objects.create(username='user1', password='1234')
        self.user2 = User.objects.create(username='user2', password='4321')
        self.new_user = User.objects.create(username='user3', password='5678')
        self.test_group.user_set.add(self.user1, self.user2)

    def test_group_user_get(self):
        response = self.client.get(f'/groups/{self.test_group.id}/users')
        self.assertIsInstance(response, JsonResponse)
        expected_data = [
            {
                'id': self.user1.id,
                'username': 'user1',
            },
            {
                'id': self.user2.id,
                'username': 'user2'
            }
        ]
        self.assertEqual(json.loads(response.content), expected_data)

    def test_group_user_get_invalid_group(self):
        response = self.client.get('/groups/0/users')
        self.assertEqual(response.status_code, 400)

    def test_group_user_post(self):
        response = self.client.post(
            f'/groups/{self.test_group.id}/user/{self.new_user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.test_group.user_set.filter(
            id=self.new_user.id).exists())

    def test_group_user_post_invalid_group(self):
        response = self.client.post(f'/groups/0/user/{self.new_user.id}')
        self.assertEqual(response.status_code, 400)

    def test_group_user_post_invalid_user(self):
        response = self.client.post(f'/groups/{self.test_group.id}/user/0')
        self.assertEqual(response.status_code, 400)

    def test_group_user_post_repeated_user(self):
        response = self.client.post(
            f'/groups/{self.test_group.id}/user/{self.user1.id}')
        self.assertEqual(response.status_code, 400)

    def test_group_user_delete(self):
        response = self.client.delete(
            f'/groups/{self.test_group.id}/user/{self.user1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user1 not in self.test_group.user_set.all())

    def test_group_user_delete_invalid_group(self):
        response = self.client.delete(f'/groups/0/user/{self.user1.id}')
        self.assertEqual(response.status_code, 400)

    def test_group_user_delete_invalid_user(self):
        response = self.client.delete(f'/groups/{self.test_group.id}/user/0')
        self.assertEqual(response.status_code, 400)

    def test_group_user_delete_user_not_exist(self):
        response = self.client.delete(
            f'/groups/{self.test_group.id}/user/{self.new_user.id}')
        self.assertEqual(response.status_code, 400)
