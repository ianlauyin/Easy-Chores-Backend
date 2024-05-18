from django.test import TestCase, Client
from django.http import JsonResponse, HttpRequest
from ..models import User
import json


class UserTestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.user1 = User.objects.create(
            username='user1', password='1234', email='user1@email.com')
        self.token = self.user1.generate_access_token()
        self.client = Client(headers={"Authorization": self.token})
        self.group1 = self.user1.groups.create(name="Group1")
        self.group2 = self.user1.groups.create(name="Group2")

    def test_user_group_get(self):
        response = self.client.get(f'/users/{self.user1.id}/groups')
        self.assertIsInstance(response, JsonResponse)
        expected_data = [
            {
                'id': self.group1.id,
                'name': self.group1.name,
            },
            {
                'id': self.group2.id,
                'name': self.group2.name
            }
        ]
        self.assertEqual(json.loads(response.content), expected_data)
