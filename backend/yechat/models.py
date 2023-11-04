from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    class Meta:
        db_table = "yechat_room"

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=50, null=True, blank=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)
    passcode = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
