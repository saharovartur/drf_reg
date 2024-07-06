from django.contrib import admin
from core.user.models import User


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['public_id', 'username', 'email', 'is_superuser']
