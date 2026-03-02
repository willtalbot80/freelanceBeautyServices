from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse


class RegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_returns_token(self):
        url = reverse('api_register')
        data = {'username': 'bob', 'password': 'pass1234', 'is_expert': False}
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertIn('token', resp.data)
        self.assertEqual(resp.data['username'], 'bob')
