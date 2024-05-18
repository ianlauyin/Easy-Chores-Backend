from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from datetime import datetime, timedelta
import jwt
import os


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(unique=False, max_length=50)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True
    )

    USERNAME_FIELD = 'email'

    def generate_access_token(self):
        data = {
            'user_id': self.id,
            'expire_time': str(datetime.now() + timedelta(hours=1))
        }
        token = jwt.encode(data, os.getenv('TOKEN_SECRET'), algorithm='HS256')
        cache.set(f'access_token_{self.id}', token, timeout=3600)
        return token

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email
