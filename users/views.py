from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, UserCreateSerializer
from utils.firebase_admin import verify_id_token
from rest_framework import exceptions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        data = UserSerializer(user).data
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED)


class ExchangeFirebaseTokenAPIView(APIView):
    """Exchange a Firebase ID token for a DRF token.

    POST payload: {"id_token": "<firebase id token>"}
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        id_token = request.data.get('id_token')
        if not id_token:
            raise exceptions.ParseError('id_token is required')

        # Prefer using the firebase backend via authenticate so behavior matches
        # `users.auth_backends.FirebaseBackend`.
        user = authenticate(request, token=id_token)
        if user is None:
            # Try direct verification error reporting
            try:
                verify_id_token(id_token)
            except Exception as e:
                raise exceptions.AuthenticationFailed(f'Invalid token: {e}')
            raise exceptions.AuthenticationFailed('Could not authenticate user')

        token, _ = Token.objects.get_or_create(user=user)
        data = UserSerializer(user).data
        data['token'] = token.key
        return Response(data, status=status.HTTP_200_OK)


class RevokeFirebaseTokensAPIView(APIView):
    """Admin endpoint to revoke a user's refresh tokens in Firebase.

    POST payload: {"uid": "<firebase uid>"} or {"email": "user@example.com"}
    Requires admin privileges in Django (`is_staff`).
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid')
        email = request.data.get('email')
        if not uid and not email:
            return Response({'detail': 'uid or email is required'}, status=status.HTTP_400_BAD_REQUEST)

        # If email provided, try to look up the Firebase uid via Django user lookup
        if not uid and email:
            try:
                user = User.objects.get(email=email)
                uid = user.username  # our FirebaseBackend stores uid in username
            except User.DoesNotExist:
                return Response({'detail': 'No local user with that email'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # This will raise if firebase not initialized or uid invalid
            auth.revoke_refresh_tokens(uid)
        except Exception as e:
            return Response({'detail': f'Failed to revoke tokens: {e}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Tokens revoked'}, status=status.HTTP_200_OK)
