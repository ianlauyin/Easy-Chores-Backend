from django.test import TestCase, Client
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.models import Group, User
from ..views.group_user_views import GroupUserViews
import json


class GroupUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.group_user = GroupUserViews()
        self.test_group = Group.objects.create(name='Test Group')
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        self.test_group.user_set.add(self.user1, self.user2)

    def test_group_user_get(self):
        response = self.group_user.get(group_id=self.test_group.id)
        self.assertIsInstance(response, JsonResponse)
        expected_data = [
            {
                'id': self.user1.id,
                'username': 'user1'
            },
            {
                'id': self.user2.id,
                'username': 'user2'
            }
        ]
        self.assertEqual(json.loads(response.content), expected_data)

    def test_group_user_get_url(self):
        response = self.client.get(f'/groups/users/{self.test_group.id}/')
        self.assertEqual(response.status_code, 200)
