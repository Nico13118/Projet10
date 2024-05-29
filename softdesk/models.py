from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150, unique=True)
    age = models.IntegerField(blank=False, default=0)
    password = models.CharField(max_length=150, blank=False)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username
