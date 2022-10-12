from django.db import models
from django.utils import timezone

# Create your models here.

class redisUser(models.Model):
    user = models.CharField(max_length=200)
    channel_name = models.CharField(max_length=600)
    active_status = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user



class chats(models.Model):
    receipt = models.CharField(max_length=400, default='None')
    chat = models.CharField(max_length=2000)
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.receipt