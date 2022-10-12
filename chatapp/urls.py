from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.authLog, name='authLog'),
    path('home', view=views.home, name='home'),
    path('chats/<str:fr>/<str:to>/<str:type>/', view=views.getChats, name='chatdata'),
    path('status/<str:user>/', view=views.getUserStaus, name='active_status'),
]
