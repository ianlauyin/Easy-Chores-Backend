from django.db import models
from django.contrib.auth.models import User, Group


class Grocery(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='groceries')
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='groceries')
    name = models.CharField(max_length=100)
    detail = models.TextField()
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
