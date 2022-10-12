from django.contrib import admin
from .models import redisUser, chats

# Register your models here.

class redisModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'channel_name', 'active_status']

admin.site.register(redisUser, redisModelAdmin)


class ChatsModelAdmin(admin.ModelAdmin):
    list_display = ['receipt', 'chat', 'time']

admin.site.register(chats, ChatsModelAdmin)