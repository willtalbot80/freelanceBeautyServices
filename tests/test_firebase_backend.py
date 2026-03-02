import os
import django

# ensure settings are configured before importing models/backends
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty.settings')
# provide dummy firebase credential for initialization
os.environ.setdefault('FIREBASE_ADMIN_CREDENTIAL', '{}')
django.setup()

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from users.auth_backends import FirebaseBackend
from unittest.mock import patch

User = get_user_model()

class FirebaseBackendTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.backend = FirebaseBackend()

    @patch('users.auth_backends.verify_id_token')
    def test_authenticate_creates_user(self, mock_verify):
        # simulate a decoded token
        mock_verify.return_value = {'uid': 'abc123', 'email': 'test@example.com'}
        request = self.factory.get('/')
        # pass token argument directly to avoid HTTP header parsing issues
        user = self.backend.authenticate(request, token='sometoken')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'abc123')
        self.assertEqual(user.email, 'test@example.com')

    @patch('users.auth_backends.verify_id_token')
    def test_invalid_token(self, mock_verify):
        mock_verify.side_effect = Exception('Bad token')
        request = self.factory.get('/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer invalid'
        user = self.backend.authenticate(request)
        self.assertIsNone(user)
