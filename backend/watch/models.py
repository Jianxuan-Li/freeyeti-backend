from django.db import models
from django.contrib.auth.models import User


class Watch(models.Model):
    title = models.CharField(max_length=100)
    video_id = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
