from django.db import models
from django.contrib.auth.models import Group
from .user import User


class Chore(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='chores')
    assigned_users = models.ManyToManyField(
        User, related_name='chores', blank=True)
    title = models.CharField(max_length=100)
    detail = models.TextField(max_length=500, default="")
    completed_date = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
