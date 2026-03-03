from rest_framework import serializers
from .models import ExpertProfile, PortfolioImage
from users.serializers import UserSerializer


class PortfolioImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioImage
        fields = ('id', 'image', 'caption', 'uploaded_at')


class ExpertProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    portfolio_images = PortfolioImageSerializer(many=True, read_only=True)

    class Meta:
        model = ExpertProfile
        fields = ('id', 'user', 'services', 'portfolio_images', 'location')
