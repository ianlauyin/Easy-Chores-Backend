from django.test import TestCase, Client
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.models import Group, User
from ..models.grocery import Grocery
from ..models.chore import Chore
import json
import datetime


class GroupTestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.client = Client()
        self.test_group = Group.objects.create(name='Test Group')
        self.user1 = User.objects.create(username='user1', password='1234')
        self.user2 = User.objects.create(username='user2', password='4321')
        self.test_group.user_set.add(self.user1, self.user2)
        self.grocery1 = Grocery.objects.create(
            creator_id=self.user1.id, group_id=self.test_group.id, name='grocery1')
        self.grocery2 = Grocery.objects.create(
            creator_id=self.user1.id, group_id=self.test_group.id, name='grocery2')
        self.chore1 = Chore.objects.create(
            group_id=self.test_group.id, title='chore1')
        self.chore2 = Chore.objects.create(
            group_id=self.test_group.id, title='chore2')
        self.chore1.assigned_users.add(self.user1, self.user2)

    def test_group_user_get(self):
        self.test_group.user_set.add(self.user1, self.user2)
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
        new_user = User.objects.create(username='user3', password='5678')
        response = self.client.post(
            f'/groups/{self.test_group.id}/user/{new_user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.test_group.user_set.filter(
            id=new_user.id).exists())

    def test_group_user_post_invalid_group(self):
        new_user = User.objects.create(username='user3', password='5678')
        response = self.client.post(f'/groups/0/user/{new_user.id}')
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

    def test_group_user_delete_invalid_user_id(self):
        response = self.client.delete(f'/groups/{self.test_group.id}/user/0')
        self.assertEqual(response.status_code, 400)

    def test_group_user_delete_user_not_exist(self):
        new_user = User.objects.create(username='user3', password='5678')
        response = self.client.delete(
            f'/groups/{self.test_group.id}/user/{new_user.id}')
        self.assertEqual(response.status_code, 400)

    def test_create_group(self):
        new_group_data = {'user_id': self.user1.id, 'name': 'New Group'}
        response = self.client.post(
            '/group', json.dumps(new_group_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        new_group = Group.objects.get(id=response_data['group_id'])
        self.assertEqual(new_group.name, 'New Group')
        self.assertEqual(new_group.user_set.first(), self.user1)

    def test_create_group_missing_name(self):
        new_group_data = {'user_id': self.user1.id}
        response = self.client.post(
            '/group', json.dumps(new_group_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Group.objects.count(), 1)

    def test_create_group_user_id(self):
        new_group_data = {'name': 'New Group'}
        response = self.client.post(
            '/group', json.dumps(new_group_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Group.objects.count(), 1)

    def test_create_group_invalid_user_id(self):
        new_group_data = {'user_id': 0, 'name': 'New Group'}
        response = self.client.post(
            '/group', json.dumps(new_group_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Group.objects.count(), 1)

    def test_get_grocery_list(self):
        response = self.client.get(f'/group/{self.test_group.id}/groceries')
        self.assertIsInstance(response, JsonResponse)
        expected_data = [{
            'created_at': self.grocery1.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z',
            'creator__username': self.user1.username,
            'id': self.grocery1.id,
            'quantity': self.grocery1.quantity
        },
            {
            'created_at': self.grocery2.created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z',
            'creator__username': self.user1.username,
            'id': self.grocery2.id,
            'quantity': self.grocery2.quantity
        }]
        self.assertEqual(json.loads(response.content), expected_data)

    def test_get_empty_grocery_list(self):
        new_group = Group.objects.create(name='New Group')
        response = self.client.get(f'/group/{new_group.id}/groceries')
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(json.loads(response.content), [])

    def test_get_grocery_list_invalid_group(self):
        response = self.client.get(f'/group/0/groceries')
        self.assertEqual(response.status_code, 400)

    def test_get_chore_list(self):
        response = self.client.get(f'/group/{self.test_group.id}/chores')
        self.assertIsInstance(response, JsonResponse)
        expected_data = [{
            'due_date': None,
            'assigned_users': [self.user1.username, self.user2.username],
            'id': self.chore1.id,
            'title': self.chore1.title
        },
            {
            'due_date': None,
            'assigned_users': [None],
            'id': self.chore2.id,
            'title': self.chore2.title
        }]
        self.assertEqual(json.loads(response.content), expected_data)

    def test_get_chore_list_without_completed(self):
        self.chore2.completed_date = datetime.datetime.now()
        self.chore2.save()
        response = self.client.get(f'/group/{self.test_group.id}/chores')
        expected_data = [{
            'due_date': None,
            'assigned_users': [self.user1.username, self.user2.username],
            'id': self.chore1.id,
            'title': self.chore1.title
        }]
        self.assertEqual(json.loads(response.content), expected_data)

    def test_get_empty_chores_list(self):
        new_group = Group.objects.create(name='New Group')
        response = self.client.get(f'/group/{new_group.id}/chores')
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(json.loads(response.content), [])

    def test_get_grocery_list_invalid_group(self):
        response = self.client.get(f'/group/0/chores')
        self.assertEqual(response.status_code, 400)
