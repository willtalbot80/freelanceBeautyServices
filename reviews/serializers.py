from rest_framework import serializers
from .models import Review
from users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    expert = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'client', 'expert', 'rating', 'comment', 'created_at')
