import email
from genericpath import exists
import json
from os import PRIO_USER
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import humanize
from .models import chats, redisUser
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView



# Create your views here.

def authLog(request):
    return render(request, 'auth.html')


def home(request):
    username = request.GET['username']
    existing_user = User.objects.filter(username=username)

    print(username, 'test-----username')


    if len(existing_user) == 0:
        User.objects.create_user(username=username, email='noeamil@gmail.com', password='password').save()
    
    IsValidUser = authenticate(username=username, password='password')
    print(IsValidUser, 'i am verification')
    
    if IsValidUser is not None:
        print(IsValidUser, 'is valid or not')
        login(request, IsValidUser)

    ChatListUsers = list(User.objects.all().exclude(username=username).exclude(username='sam').exclude(username__contains='group').values('username'))
    ChatGroupList = list(User.objects.filter(username__contains='group').values('username'))
    
    return render(request, 'home.html', {'chatUserList' : ChatListUsers, 'groupList': ChatGroupList})


def getChats(request, fr, to, type):
    rfrom = fr+'_'+to
    rto = to+'_'+fr

    if type == 'private':
        saved_chats = chats.objects.filter(receipt__in=[str(rfrom), str(rto)])

    elif type == 'group':
        saved_chats = chats.objects.filter(receipt__regex=to)

    data_dict = {'chats':list(saved_chats.values())}
    
    data = json.dumps(data_dict, indent=0, sort_keys=True, default=str)

    return JsonResponse(data, safe=False)

def getUserStaus(request, user):
    user_status = redisUser.objects.filter(user=user).values('active_status').get()['active_status']

    if user_status != None:
        last_online = redisUser.objects.filter(user=user).values('active_status').get()['active_status']
        user_status = humanize.naturaltime(timezone.datetime.now(timezone.utc) - last_online)

    return JsonResponse(user_status, safe=False)


    
    


