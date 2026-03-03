from rest_framework import serializers
from .models import Appointment
from users.serializers import UserSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    client = UserSerializer(read_only=True)
    expert = UserSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'client', 'expert', 'start', 'end', 'status', 'notes', 'created_at')
