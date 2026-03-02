import json
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from unittest import mock


User = get_user_model()


def test_exchange_firebase_token_creates_token(monkeypatch, db):
    client = APIClient()

    # create a user that our mocked authenticate will return
    user = User.objects.create_user(username='fbuid123', email='test@example.com', password='unused')

    # mock authenticate to return our user when called with token
    def fake_authenticate(request, token=None):
        if token == 'valid-test-token':
            return user
        return None

    monkeypatch.setattr('django.contrib.auth.authenticate', fake_authenticate)

    url = reverse('api_exchange_firebase_token')
    resp = client.post(url, data={'id_token': 'valid-test-token'}, format='json')
    assert resp.status_code == 200
    data = resp.json()
    assert 'token' in data
    assert data['email'] == 'test@example.com'
