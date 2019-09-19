import json
import ojuser
import account
from announcement.models import Announcement
from ojuser import serializers
from rest_framework_jwt.utils import jwt_decode_handler
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from ojuser.models import GroupProfile, UserProfile
from problem.models import Problem, ProblemDataInfo, ProblemCase
from problem.filters import ProblemFilter
from problem.tables import ProblemTable
from problem.serializers import ProblemSerializer, ProblemDataInfoSerializer
from problem.serializers import FileSerializer, ProblemDataSerializer, ProblemCaseSerializer
from problem.forms import ProblemForm
from guardian.shortcuts import get_objects_for_user
from django_tables2 import RequestConfig
from ojuser.models import GroupProfile
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware import csrf
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password

# This is The API for The Frontend
# Old API is not Here
# Comment is Above the Code
# In Fact Most of The Code Is Copy From the Old Code
# However I am not Able to Understand How to Use Them
# So I Copy and Modify Them

'''
    Given A User's Name,Return His Information
'''


def GetUserInfo(name):
    context = {}
    try:
        user = User.objects.select_related('profile').get(username=name)
    except Exception:
        context['status'] = "User named '{}' does not exist".format(name)
        return HttpResponse(json.dumps(context))

    context['status'] = "OK"

    context['username'] = name

    context['email'] = user.email
    context['is_superuser'] = user.is_superuser
    context['is_staff'] = user.is_staff
    context['is_active'] = user.is_active

    context['is_teacher'] = user.profile.is_teacher
    context['nickname'] = user.profile.nickname
    sex = user.profile.gender
    if sex == 'F':
        context['gender'] = "Female"
    elif sex == 'M':
        context['gender'] = "Male"
    else:
        context['gender'] = "Secret"
    return context


'''
API /rinne/QueryUser
Get Some User's Information
'''


def QueryUser(request):
    username = request.GET.get("username")
    return HttpResponse(json.dumps(GetUserInfo(username)))


'''
API /rinne/SelfInfo
Get Current Logged User's Information
'''


def SelfInfo(request):
    name = request.user.username
    return HttpResponse(json.dumps(GetUserInfo(name)))


'''
API /rinne/GetProblemList
return list of problem list
'''


def GetProblemList(request):
    key = int(request.GET.get("key")) if 'key' in request.GET else ""
    context = {}
    gp_can_view = get_objects_for_user(
        request.user,
        'ojuser.view_groupprofile',
        with_superuser=True
    )
    problem_can_view_qs = Problem.objects.filter(title__icontains=key, groups__in=gp_can_view).distinct()

    gp_can_change = get_objects_for_user(
        request.user,
        'ojuser.change_groupprofile',
        with_superuser=True
    )
    problem_can_change_qs = Problem.objects.filter(title__icontains=key, groups__in=gp_can_change).distinct()

    groups_can_delete = get_objects_for_user(
        request.user,
        'problem.delete_problem',
        with_superuser=True
    )
    problem_can_delete_qs = Problem.objects.filter(title__icontains=key, pk__in=groups_can_delete).distinct()

    problem_can_change_qs |= problem_can_delete_qs
    problem_can_view_qs |= problem_can_change_qs
    context['status'] = "OK"
    context['from'] = request.user.username
    context['problem'] = [{"solved": False, "uid": i.id, "name": i.title, "time_limit": i.time_limit, "memory_limit": i.memory_limit, "superadmin": i.superadmin.username} for i in problem_can_view_qs]
    return HttpResponse(json.dumps(context))


'''
API /rinne/GetProblem
Given A ID return corresponding problem infomation
'''


def GetProblem(request):
    context = {}
    if 'index' not in request.GET:
        context['status'] = "Index Cannot Be Blank"
    elif request.user.is_authenticated():
        uid = request.GET.get("index")
        problem_set = Problem.objects.filter(id=uid).distinct()
        assert(len(problem_set) == 1)
        foo = problem_set[0]
        if request.user.has_perm('problem.change_problem', foo):
            context['status'] = "OK"
            context['title'] = request.user.username
            context['from'] = request.user.username
            context['id'] = foo.id
            context['time_limit'] = foo.time_limit
            context['memory_limit'] = foo.memory_limit
            context['code_length_limit'] = foo.code_length_limit
            context['desc'] = foo.desc
            context['is_checked'] = foo.is_checked
            context['superadmin'] = foo.superadmin.username
            context['created_time'] = foo.created_time.strftime('%Y/%m/%d %h %I:%M:%S%p')
            context['last_updated_time'] = foo.last_updated_time.strftime('%Y/%m/%d %h %I:%M:%S%p')
            context['groups'] = foo.groups.name
            context['tags'] = foo.tags.name
            context['is_spj'] = foo.is_spj
        else:
            context['status'] = "What Are You Going To Do?"
    else:
        context['status'] = "You Are Not Log in"
    return HttpResponse(json.dumps(context))


'''
API /rinne/GetAnnouncementList
Given the page, return corresponding list of Announcement list
'''


def GetAnnouncement(request):
    context = {}
    if 'index' in request.GET:
        uid = request.GET.get("index")
        res = Announcement.objects.filter(pk=uid)
        if res:
            data = res[0]
            context['status'] = "OK"
            context['pk'] = data.pk
            context['title'] = data.title
            context['content'] = data.content
            context['author'] = data.author.username
            context['create_time'] = data.create_time.strftime('%Y/%m/%d %h %I:%M:%S%p')
            context['update_time'] = data.update_time.strftime('%Y/%m/%d %h %I:%M:%S%p')
            context['is_sticky'] = data.is_sticky
            context['last_update_user'] = data.last_update_user.username
        else:
            context['status'] = "No Such Announcement"
    else:
        context['status'] = "Index Cannot Be Blank"
    return HttpResponse(json.dumps(context))


'''
API /rinne/GetAnnouncement
Given the index, return corresponding Announcement
'''


def GetAnnouncementList(request):
    context = {}
    context['status'] = "OK"
    announcements = Announcement.objects.order_by('-is_sticky', '-update_time').all()
    context['data'] = [{
        "pk": i.pk,
        "title": i.title,
        "author": i.author.username,
        "brief": i.content[:50],
        "update_time": i.update_time.strftime("%Y/%m/%d %h %I:%M:%S%p"),
        "is_sticky": i.is_sticky
    } for i in announcements]
    return HttpResponse(json.dumps(context))


'''
Useless Just for Test
'''
@ensure_csrf_cookie
def test(request):
    context = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    return HttpResponse(json.dumps(context))


'''
API /rinne/Login
Attempt to Login
'''


def Login(request):
    context = {}
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        context['status'] = "OK"
        context['data'] = GetUserInfo(user.username)
        login(request, user)
    else:
        context['status'] = "Login Failed"
    return HttpResponse(json.dumps(context))


'''
API /rinne/Register
Attempt to Register
'''


def Register(request):
    context = {}
    username = request.POST.get('username')
    password = request.POST.get('password')
    nickname = request.POST.get('nickname')
    gender = request.POST.get('gender')[0]
    email = request.POST.get('email')
    u = User.objects.filter(username=username)
    v = User.objects.filter(email=email)
    if u:
        context['status'] = 'User has existed'
    elif v:
        context['status'] = 'Email has existed'
    else:
        context['status'] = 'OK'
        u = User.objects.create_user(username=username, email=email, password=password)
        profile = u.profile
        profile.nickname = nickname
        profile.gender = gender
        profile.save()
        u.save()
    return HttpResponse(json.dumps(context))


'''
API /rinne/GetCSRF
Return CSRF Token
'''


def GetCSRF(request):
    context = {}
    token = csrf.get_token(request)
    print("csrf:", token)
    context['CSRFToken'] = token
    return HttpResponse(json.dumps(context))


'''
API /rinne/ChangeUserInfo
Change User's Basic Infomation
'''


def ChangeUserInfo(request):
    context = {}
    name = request.GET.get('username')
    gender = request.GET.get('gender')
    nickname = request.GET.get('nickname')
    email = request.GET.get('email')

    operate_user = request.user
    if operate_user.username == name or operate_user.is_staff:
        u = User.objects.select_related('profile').get(username=name)
        if u:
            profile = u.profile
            profile.gender = gender[0]
            profile.nickname = nickname
            profile.save()
            u.email = email
            u.save()
            context["status"] = "OK"
        else:
            context["status"] = "No Such User"
    else:
        context["status"] = "You are not allowed to do this"
    return HttpResponse(json.dumps(context))


'''
API /rinne/ChangeUserPass
Change User's Password
'''


def ChangeUserPass(request):
    context = {}
    name = request.GET.get('username')
    old_pass = request.GET.get('old_pass')
    new_pass = request.GET.get('new_pass')

    operate_user = request.user
    if operate_user.username == name or operate_user.is_staff:
        u = User.objects.filter(username=name)
        if u:
            if authenticate(username=name, password=old_pass):
                u.set_password(new_pass)
                u.save()
                context["status"] = "OK"
            else:
                context["status"] = "Old Password is Wrong"
        else:
            context["status"] = "No Such User"
    else:
        context["status"] = "You are not allowed to do this"
    return HttpResponse(json.dumps(context))


'''
API /rinne/ChangeUserPower
# Need Authentication Check,Important
Change User's Power,etc Teacher Admin and Active
'''


def ChangeUserPower(request):
    # return HttpResponse("123")
    context = {}
    name = request.GET.get('username')
    is_staff = request.GET.get('is_staff')
    is_teacher = request.GET.get('is_teacher')
    is_active = request.GET.get('is_active')
    operate_user = request.user
    if operate_user.username == name or operate_user.is_staff:
        u = User.objects.select_related('profile').get(username=name)
        if u:
            profile = u.profile
            profile.is_teacher = (is_teacher == "true")
            u.is_staff = (is_staff == "true")
            u.is_active = (is_active == "true")
            profile.save()
            u.save()
            context["status"] = "OK"
        else:
            context["status"] = "No Such User"
    else:
        context["status"] = "You are not allowed to do this"
    return HttpResponse(json.dumps(context))
