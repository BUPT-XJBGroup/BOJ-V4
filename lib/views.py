from rest_framework_jwt.utils import jwt_decode_handler
from django.shortcuts import render
import json
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

    context['email'] = user.profile.user.email
    context['is_superuser'] = user.profile.user.is_superuser
    context['is_staff'] = user.profile.user.is_staff
    context['is_active'] = user.profile.user.is_active

    context['is_teacher'] = user.profile.is_teacher
    context['nickname'] = user.profile.nickname
    sex = user.profile.gender
    if sex == 'F':
        context['gender'] = "Female"
    elif sex == 'M':
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
    name = request.user.username
    return GetUserInfo(name)


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


def GetAnnouncementList(request):
    context = [1]
    return HttpResponse(json.dumps(context))


'''
API /rinne/GetAnnouncement
Given the index, return corresponding Announcement
'''


def GetAnnouncement(request):
    context = [1]
    return HttpResponse(json.dumps(context))


def test(request):
    context = [1]
    return HttpResponse(json.dumps(context))
