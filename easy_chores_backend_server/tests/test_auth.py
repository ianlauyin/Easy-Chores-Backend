from django.test import TestCase, Client
from django.http import HttpRequest, JsonResponse
from django.http.request import HttpRequest
from ..views.auth_views import verify_token
import json
from ..models import User
from django.core.cache import cache
import os
import jwt


class AuthTestCase(TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword')
        self.token = self.user.generate_access_token()

    def test_register_with_valid_data(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        }
        response = self.client.post(
            '/users/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertEqual(cache.get(f'access_token_{User.objects.get(
            email="test@example.com").id}'), response.json()['access_token'])

    def test_register_with_missing_data(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(
            '/users/register', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(
            username='test@example.com').exists())

    def test_register_with_invalid_json(self):
        data = 'invalid json'
        response = self.client.post(
            '/users/register', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_success(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(
            '/users/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())

        access_token = response.json()['access_token']
        payload = jwt.decode(access_token, os.getenv(
            'TOKEN_SECRET'), algorithms=['HS256'])
        self.assertEqual(payload['user_id'], self.user.id)

    def test_login_missing_email(self):
        data = {
            'password': 'testpassword'
        }
        response = self.client.post(
            '/users/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_missing_password(self):
        data = {
            'email': 'testuser@example.com'
        }
        response = self.client.post(
            '/users/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_login_invalid_password(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(
            '/users/login', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_invalid_json(self):
        response = self.client.post(
            '/users/login', data='invalid json', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_valid_token(self):
        @verify_token
        def test_view(request):
            return JsonResponse({'message': 'Success'})

        request = HttpRequest()
        request.headers = {'Authorization': self.token}
        response = test_view(request)
        self.assertIsInstance(response, JsonResponse)
