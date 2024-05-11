from django.test import TestCase, Client
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.models import Group, User
from ..models import Chore
import json
import datetime


class ChoreTestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.client = Client()
        self.group = Group.objects.create(name='Test Group')
        self.chore = Chore.objects.create(group=self.group, title='Test title')
        self.user1 = User.objects.create(username='user1')
        self.chore.assigned_users.add(self.user1)

    def test_chore_view_get(self):
        response = self.client.get(f'/chores/{self.chore.id}')
        self.assertIsInstance(response, JsonResponse)
        response_data: dict[str] = json.loads(response.content)
        expected_data = {
            'id': self.chore.id,
            'title': self.chore.title,
            'detail': self.chore.detail,
            'completed_date': None,
            'assigned_users': [{'id': self.user1.id, 'username': self.user1.username}],
            'group': self.group.id
        }
        self.assertDictEqual(response_data, expected_data)

    def test_chore_view_get_without_user(self):
        self.chore.assigned_users.remove(self.user1)
        response = self.client.get(f'/chores/{self.chore.id}')
        response_data: dict[str] = json.loads(response.content)
        expected_data = {
            'id': self.chore.id,
            'title': self.chore.title,
            'detail': self.chore.detail,
            'completed_date': None,
            'assigned_users': [],
            'group': self.group.id
        }
        self.assertDictEqual(response_data, expected_data)

    def test_chore_view_get_invalid_id(self):
        response = self.client.get('/chores/0')
        self.assertEqual(response.status_code, 404)

    def test_chore_view_post(self):
        new_chore_data = {'group_id': self.group.id, 'title': 'New Test Title'}
        response = self.client.post(
            '/chores', json.dumps(new_chore_data), content_type='application/json')
        self.assertIsInstance(response, JsonResponse)
        response_data: dict[str] = json.loads(response.content)
        self.assertIn('id', response_data)
        new_chore = Chore.objects.filter(id=response_data['id'])
        self.assertTrue(new_chore.exists())
        new_chore_values = new_chore.values().get()
        self.assertEqual(new_chore_values['title'], 'New Test Title')
        self.assertEqual(new_chore_values['detail'], '')
        self.assertIsNone(new_chore_values['completed_date'])
        self.assertEqual(new_chore_values['group_id'], self.group.id)
        self.assertFalse(new_chore.get().assigned_users.all().exists())

    def test_chore_view_post_with_detail(self):
        new_chore_data = {'group_id': self.group.id,
                          'title': 'New Test Title', 'detail': 'New Test Detail'}
        response = self.client.post(
            '/chores', json.dumps(new_chore_data), content_type='application/json')
        self.assertIsInstance(response, JsonResponse)
        response_data: dict[str] = json.loads(response.content)
        self.assertIn('id', response_data)
        new_chore = Chore.objects.filter(id=response_data['id'])
        self.assertTrue(new_chore.exists())
        new_chore_values = new_chore.values().get()
        self.assertEqual(new_chore_values['title'], 'New Test Title')
        self.assertEqual(new_chore_values['detail'], 'New Test Detail')
        self.assertIsNone(new_chore_values['completed_date'])
        self.assertEqual(new_chore_values['group_id'], self.group.id)
        self.assertFalse(new_chore.get().assigned_users.all().exists())

    def test_chore_view_post_invalid_group_id(self):
        new_chore_data = {'group_id': 0,
                          'title': 'New Test Title'}
        response = self.client.post(
            '/chores', json.dumps(new_chore_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_chore_view_post_missing_group_id(self):
        new_chore_data = {'title': 'New Test Title'}
        response = self.client.post(
            '/chores', json.dumps(new_chore_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_chore_view_post_missing_title(self):
        new_chore_data = {'group_id': self.group.id}
        response = self.client.post(
            '/chores', json.dumps(new_chore_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_chore_view_put(self):
        update_data = {
            'title': 'Updated Test Chore',
            'detail': 'Updated Test Detail',
            'completed_date': datetime.datetime.now().isoformat()
        }
        response = self.client.put(
            f'/chores/{self.chore.id}', json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.title, update_data['title'])
        self.assertEqual(self.chore.detail, update_data['detail'])
        self.assertEqual(self.chore.completed_date.isoformat(),
                         update_data['completed_date'][:10])

    def test_chore_view_put_only_title(self):
        update_data = {
            'title': 'Updated Test Chore',
        }
        response = self.client.put(
            f'/chores/{self.chore.id}', json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.title, update_data['title'])
        self.assertEqual(self.chore.detail, '')
        self.assertIsNone(self.chore.completed_date)

    def test_chore_view_put_wrong_type_title(self):
        update_data = {
            'title': 1234,
        }
        response = self.client.put(
            f'/chores/{self.chore.id}', json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_chore_view_put_wrong_type_detail(self):
        update_data = {
            'title': 'Updated Test Title',
            'detail': 1234
        }
        response = self.client.put(
            f'/chores/{self.chore.id}', json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_chore_view_put_wrong_type_date(self):
        update_data = {
            'title': 'Updated Test Title',
            'completed_date': 'date'
        }
        response = self.client.put(
            f'/chores/{self.chore.id}', json.dumps(update_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_chore_view_delete(self):
        response = self.client.delete(f'/chores/{self.chore.id}')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Chore.objects.filter(id=self.chore.id).exists())

    def test_chore_view_delete_invalid_id(self):
        response = self.client.delete(f'/chores/0')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Chore.objects.count(), 1)

    def test_rearrange_chores_assigned_users_remove(self):
        response = self.client.put(
            f'/chores/{self.chore.id}/users', json.dumps({'user_ids': []}), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.assigned_users.count(), 0)

    def test_rearrange_chores_assigned_users_add(self):
        new_user = User.objects.create(username='New User')
        response = self.client.put(
            f'/chores/{self.chore.id}/users', json.dumps({'user_ids': [self.user1.id, new_user.id]}), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.assigned_users.count(), 2)

    def test_rearrange_chores_assigned_users_changed(self):
        new_user = User.objects.create(username='New User')
        response = self.client.put(
            f'/chores/{self.chore.id}/users', json.dumps({'user_ids': [new_user.id]}), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.assigned_users.count(), 1)
        self.assertEqual(self.chore.assigned_users.first(), new_user)

    def test_rearrange_chores_assigned_users_invalid_id(self):
        response = self.client.put(
            f'/chores/0/users', json.dumps({'user_ids': []}), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.assigned_users.count(), 1)
        self.assertEqual(self.chore.assigned_users.first(), self.user1)

    def test_rearrange_chores_assigned_users_wrong_type(self):
        response = self.client.put(
            f'/chores/{self.chore.id}/users', json.dumps({'user_ids': ['one']}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.assigned_users.count(), 1)
        self.assertEqual(self.chore.assigned_users.first(), self.user1)
