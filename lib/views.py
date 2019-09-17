from rest_framework_jwt.utils import jwt_decode_handler
from django.shortcuts import render
import json
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from ojuser.models import GroupProfile, UserProfile
# This is The API for The Frontend
# Old API is not Here
'''
    Given A User's Name,Return His Information
'''
def GetUserInfo(name):
    context={}
    try:
        user = User.objects.select_related('profile').get(username=name)
    except Exception:
        context['status'] = "User named '{}' does not exist".format(name)
        return HttpResponse(json.dumps(context))

    context['status'] = "OK"

    context['username'] = name

    context['email'] = user.profile.user.email
    context['is_superuser'] = user.profile.user.is_superuser
    context['is_staff'] = user.profile.user.is_staff
    context['is_active'] = user.profile.user.is_active

    context['is_teacher'] = user.profile.is_teacher
    context['nickname'] = user.profile.nickname
    sex=user.profile.gender
    if sex=='F':
        context['gender'] = "Female"
    elif sex=='M':
        context['gender'] = "Male"
    else:
        context['gender'] = "Secret"
    return HttpResponse(json.dumps(context))

'''
API /rinne/QueryUser
Get Some User's Information
'''

def QueryUser(request):
    username = request.GET.get("username")
    return GetUserInfo(username)

'''
API /rinne/SelfInfo
Get Current Logged User's Information
'''

def SelfInfo(request):
    name = request.user.profile.user.username
    return GetUserInfo(name)
