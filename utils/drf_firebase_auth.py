from rest_framework import authentication, exceptions
from django.contrib.auth import authenticate


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None
        token = parts[1]
        user = authenticate(request, token=token)
        if not user:
            raise exceptions.AuthenticationFailed('Invalid Firebase token')
        return (user, None)
