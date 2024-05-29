from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'age',
        'can_be_contacted', 'can_data_be_shared',
        'is_active', 'is_staff', 'is_superuser')


admin.site.register(User, UserAdmin)
