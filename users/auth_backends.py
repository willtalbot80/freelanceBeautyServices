from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from utils.firebase_admin import verify_id_token

User = get_user_model()


class FirebaseBackend(BaseBackend):
    """Authenticate using Firebase ID token provided in Authorization header.

    Expects token type 'Bearer <id_token>'.
    """

    def authenticate(self, request, token=None):
        if token is None:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
        if not token:
            return None
        try:
            decoded = verify_id_token(token)
        except Exception:
            return None
        uid = decoded.get('uid')
        email = decoded.get('email')
        if not email:
            return None
        user, _ = User.objects.get_or_create(username=uid, defaults={'email': email})
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
