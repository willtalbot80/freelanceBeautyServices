from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import ExpertProfile, PortfolioImage
from .serializers import ExpertProfileSerializer, PortfolioImageSerializer
from django.shortcuts import render, get_object_or_404
from users.permissions import IsExpert, IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied


class ExpertProfileViewSet(viewsets.ModelViewSet):
    queryset = ExpertProfile.objects.select_related('user').all()
    serializer_class = ExpertProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PortfolioImageViewSet(viewsets.ModelViewSet):
    queryset = PortfolioImage.objects.select_related('expert__user').all()
    serializer_class = PortfolioImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly, IsExpert]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'expert_profile') or not user.is_expert:
            raise PermissionDenied('Only experts can upload portfolio images')
        serializer.save(expert=user.expert_profile)


def expert_list(request):
    qs = ExpertProfile.objects.select_related('user').prefetch_related('portfolio_images').all()
    return render(request, 'experts/list.html', {'experts': qs})


def expert_detail(request, pk):
    profile = get_object_or_404(ExpertProfile.objects.select_related('user').prefetch_related('portfolio_images'), pk=pk)
    return render(request, 'experts/detail.html', {'profile': profile})
