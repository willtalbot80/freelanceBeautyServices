from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users.views import UserViewSet, RegisterAPIView
from users.views import ExchangeFirebaseTokenAPIView
from experts.views import ExpertProfileViewSet, PortfolioImageViewSet, expert_list, expert_detail
from appointments.views import AppointmentViewSet
from reviews.views import ReviewViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'experts', ExpertProfileViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'portfolio-images', PortfolioImageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/exchange-firebase-token/', ExchangeFirebaseTokenAPIView.as_view(), name='api_exchange_firebase_token'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # simple pages
    path('', expert_list, name='expert_list'),
    path('experts/<int:pk>/', expert_detail, name='expert_detail'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
