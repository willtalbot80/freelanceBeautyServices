from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from io import BytesIO
from PIL import Image


User = get_user_model()


def make_image_file():
    f = BytesIO()
    Image.new('RGB', (10, 10)).save(f, 'JPEG')
    f.name = 'test.jpg'
    f.seek(0)
    return f


class PortfolioUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('expert1', password='pass', is_expert=True)
        # create profile
        from experts.models import ExpertProfile
        ExpertProfile.objects.create(user=self.user)

    def test_upload_portfolio_image(self):
        # obtain token
        from rest_framework.authtoken.models import Token
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        url = reverse('portfolioimage-list')
        img = make_image_file()
        resp = self.client.post(url, {'image': img, 'caption': 'demo'}, format='multipart')
        self.assertEqual(resp.status_code, 201)
        self.assertIn('id', resp.data)
