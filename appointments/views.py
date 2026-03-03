from rest_framework import viewsets, permissions
from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('client', 'expert').all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # default behavior: set client to the requesting user if not provided
        if not serializer.validated_data.get('client'):
            serializer.save(client=self.request.user)
        else:
            serializer.save()
