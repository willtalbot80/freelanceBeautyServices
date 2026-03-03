from django.contrib import admin
from .models import ExpertProfile, PortfolioImage


@admin.register(ExpertProfile)
class ExpertProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location')


@admin.register(PortfolioImage)
class PortfolioImageAdmin(admin.ModelAdmin):
    list_display = ('expert', 'image', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
