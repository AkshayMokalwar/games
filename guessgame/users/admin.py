from django.contrib import admin

# Register your models here.
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_score', 'avatar', 'lifelines_remaining')
    search_fields = ('user__username',)
    list_filter = ('lifelines_remaining',)
    readonly_fields = ('total_score',)