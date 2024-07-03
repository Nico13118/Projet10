from django.db import models, transaction
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150, unique=True)
    age = models.IntegerField(blank=False, default=0)
    password = models.CharField(max_length=150, blank=False)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Project(models.Model):
    objects = models.Manager()
    TYPE = [
        ('BA', 'back-end'),
        ('FE', 'front-end'),
        ('IOS', 'iOS'),
        ('AND', 'Android')
    ]
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='project_author')
    contributors = models.ManyToManyField('User', through='Contributor', related_name='project_contributor')
    project_name = models.CharField(max_length=200, blank=False)
    project_description = models.TextField(max_length=8192, blank=False)
    type = models.CharField(max_length=3, choices=TYPE, blank=False)

    def __str__(self):
        return self.project_name


class Contributor(models.Model):
    objects = models.Manager()
    date_joined = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='contributor_user')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='contributor_project')

    def __str__(self):
        return f"{self.user} - {self.project}"
