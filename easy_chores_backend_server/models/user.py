from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


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

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        super().set_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email
