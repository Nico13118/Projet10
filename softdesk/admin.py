from django.contrib import admin
from softdesk.models import User, Project, Contributor


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'age',
        'can_be_contacted', 'can_data_be_shared',
        'is_active', 'is_staff', 'is_superuser'
    )
    ordering = ('id',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created_time', 'author', 'project_name',
        'project_description', 'type'
    )
    ordering = ('id',)


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'date_joined', 'user', 'project'
    )
    ordering = ('id',)

