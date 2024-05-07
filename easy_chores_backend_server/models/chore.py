from django.db import models
from django.contrib.auth.models import User, Group


class Chore(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='chores')
    assigned_users = models.ManyToManyField(
        User, related_name='chores')
    title = models.CharField(max_length=100)
    detail = models.TextField(max_length=500)
    completed_date = models.DateField(null=True)
    due_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title