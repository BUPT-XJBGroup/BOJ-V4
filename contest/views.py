#encoding: utf-8
from datetime import datetime, timedelta
import json
import math
import base64
from functools import wraps

from .models import Contest, ContestProblem, Submission, Notification, Clarification\
    , ProblemRecord, BoradRecord
from .filters import ContestFilter, SubmissionFilter
from .tables import ContestTable, NotificationTable, ClarificationTable, SubmissionTable
from .forms import ContestForm, SubmissionForm, NotificationForm, QuestionForm, AnswerForm
from .serializers import ContestSerializer
from problem.models import Problem
from bojv4.conf import LANGUAGE_MASK, CONTEST_TYPE, CONTEST_CACHE_EXPIRE_TIME, CONTEST_CACHE_FLUSH_TIME, CONTEST_TYPE_ICPC, CONTEST_TYPE_ICPC_MANUAL, CONTEST_TYPE_OI
from common.nsq_client import send_to_nsq
from cheat.models import Record
from ojuser.models import GroupProfile

from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from guardian.shortcuts import get_objects_for_user

from django_tables2 import RequestConfig

from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.request import Request

from ojuser.utils import get_users_with_perm

import logging
logger = logging.getLogger('django')
# Create your views here.


class ContestViewPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, Contest):
            return False
        if request.user.has_perm('ojuser.change_groupprofile', obj.group):
            return True
        now = datetime.now()
        if request.user.has_perm('ojuser.view_groupprofile', obj.group) and obj.ended() != -1:
            return True
        return False


def view_permission_required(func):

    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):
            pk = kwargs.get('pk')
            contest = Contest.objects.filter(pk=pk).first()
            if pk and contest:
                if request.user.has_perm('ojuser.view_groupprofile', contest.group):
                    return func(request, *args, **kwargs)
                elif request.user.has_perm('ojuser.change_groupprofile', contest.group):
                    return func(request, *args, **kwargs)
            raise PermissionDenied
        return returned_wrapper
    if not func:
        def foo(func):
            return decorator(func)
        return foo
    return decorator(func)


def check_permission(user, contest):
    if not user.has_perm('ojuser.view_groupprofile', contest.group):
        raise PermissionDenied


class ContestViewSet(ModelViewSet):
    queryset = Contest.objects.all()
    permission_classes = (IsAuthenticated, ContestViewPermission)
    serializer_class = ContestSerializer
    @detail_route(methods=['post'], url_path='submit')
    def submit(self, request, pk=None):
        if self.get_object().ended() != 0 and not request.user.has_perm('ojuser.change_groupprofile', self.get_object().group):
            messages.add_message(
                self.request._request,
                messages.ERROR,
                _(u'考试已结束')
            )
            return Response({'code': -1})
        if Problem.is_forbid(request.user):
            messages.add_message(
                self.request._request,
                messages.ERROR,
                _(u'因为恶意操作， 您已被禁止提交')
            )
            raise PermissionDenied
        judgeRequest = request.data.dict()
        judgeRequest['user'] = request.user.id
        judgeRequest['submit_ip'] = request.META.get('REMOTE_ADDR', None)
        # send_to_nsq('submit', json.dumps(request.data))
        send_to_nsq('submit', json.dumps(judgeRequest))
        messages.add_message(
            self.request._request,
            messages.SUCCESS,
            _(u'提交成功')
        )
        return Response({'code': 0})

    @detail_route(methods=['get'], url_path='cheat')
    def cheat(self, request, pk=None):
        if self.get_object().ended() != 1:
            messages.add_message(
                self.request._request,
                messages.ERROR,
                _('Contest has not ended.')
            )
            return Response({'code': -1})
        if not self.get_object().change_by_user(request.user):
            raise PermissionDenied

        for p in self.get_object().problems.all():
            send_to_nsq('cheat', str(p.pk))
        messages.add_message(
            self.request._request,
            messages.SUCCESS,
            _('cheat has started')
        )
        return Response({'code': 0})

    @detail_route(methods=['get'], url_path='clear')
    def clear_record(self, request, pk=None):
        if not self.get_object().change_by_user(request.user):
            raise PermissionDenied
        for p in self.get_object().problems.all():
            p.cheat.all().delete()
        messages.add_message(
            self.request._request,
            messages.SUCCESS,
            _('cheat record has been cleaned')
        )
        return Response({'code': 0})

    def get_board_from_cache(self, group_id, data):
        if not group_id:
            return data
        group = GroupProfile.objects.filter(pk=group_id).first()
        if not group:
            return data
        users = set(group.user_group.user_set.all().values_list('username'))
        if not isinstance(data, list):
            data = json.loads(data)
        return filter(lambda x: (x['username'],) in users, data)

    @detail_route(methods=['get'], url_path='board')
    def get_contest_board(self, request, pk=None):
        group_id = request.GET.get('group_id', None)
        real_time = request.GET.get('real_time', 0) > 0

        contest = self.get_object()

        # Get users who have permission change_groupprofile to the current contest's group
        admins = set(get_users_with_perm(contest.group, 'change_groupprofile', True, True))

        # Only admin can view the real_time board
        if real_time and not request.user in admins:
            if contest.ended() == 0 or contest.contest_type == CONTEST_TYPE_ICPC_MANUAL:
                raise PermissionDenied

        rt_prefix = "__rt" if real_time else ""
        lock = str(contest.pk) + rt_prefix + "__lock"
        cache_key = contest.key() + rt_prefix
        if cache.get(lock):
            res = cache.get(cache_key)
            return Response(self.get_board_from_cache(group_id, res))
        cache.set(lock, 1, CONTEST_CACHE_FLUSH_TIME)
        # cache.set(lock, 1, 1)

        # Calculate the board

        submission_filter = {
            "problem__contest" : contest,
            "user__is_superuser" : False,
        }

        if not real_time:
            submission_filter["create_time__lt"] = contest.get_board_seal_time()

        subs = Submission.objects.select_related("user", "user__profile", "problem")\
            .filter(**submission_filter).order_by("create_time")\
            .all()
        probs = ContestProblem.objects.select_related("problem").filter(contest=contest).all()

        solved_problem = set()

        mp = {}
        for p in probs:
            mp[p.index] = float(p.score) / max(1, p.problem.score)
        info = {}
        for sub in subs:
            uid = sub.user.username
            idx = sub.problem.index
            # if sub.status in ['PD', 'JD', 'CL', 'SE'] or sub.user.has_perm('ojuser.change_groupprofile', contest.group):
            if sub.status in ['PD', 'JD', 'CL', 'SE', 'CE'] or sub.user in admins:
                continue
            if uid not in info:
                # info[uid] = {'username': uid, 'nickname': sub.user.profile.nickname}
                info[uid] = BoradRecord(username=uid, nickname=sub.user.profile.nickname)
            uinfo = info[uid]
            pinfo = uinfo.problems
            if idx not in pinfo:
                pinfo[idx] = ProblemRecord(idx)
            sinfo = pinfo[idx]
            if sinfo.AC > 0:
                continue
            sinfo.sub += 1
            if sub.status == "AC":
                sinfo.AC = sinfo.sub
                td = sub.create_time - contest.start_time
                sinfo.ac_time = int(math.ceil(td.total_seconds() / 60))
                # info[uid]['pinfo'][idx]["pen"] += int(math.ceil(td.total_seconds() / 60))

                # Mark the problem as solved. If current submission is the first solve of the problem, mark as first blood
                if not sub.problem.index in solved_problem:
                    sinfo.first_blood = True
                    solved_problem.add(sub.problem.index)
            else:
                sinfo.AC -= 1
                if contest.type_is_icpc():
                    sinfo.pen += 20
            if contest.type_is_oi():
                sinfo.pen = max(sinfo.pen, int(mp[idx] * sub.score))
        info = info.values()
        calc_contest_type = CONTEST_TYPE_ICPC
        if contest.type_is_oi():
            calc_contest_type = CONTEST_TYPE_OI
        for v in info:
            v.calc(probs, calc_contest_type)
        if contest.type_is_icpc():
            info.sort(key=lambda x: x.AC*1000000 - x.pen, reverse=True)
        else:
            info.sort(key=lambda x: x.pen, reverse=True)
        ans = [x.to_json() for x in info]


        # scoreMap = {}
        # for p in probs:
        #     scoreMap[p.id] = float(p.score) / max(1, p.problem.score)

        cache.set(cache_key, ans, CONTEST_CACHE_EXPIRE_TIME)
        return Response(self.get_board_from_cache(group_id, ans))


    @detail_route(methods=['post'], url_path='release-board')
    def release_final_board(self, request, pk=None):
        contest = self.get_object()
        if contest.contest_type != CONTEST_TYPE_ICPC_MANUAL:
            raise Http404
        if not request.user.has_perm('ojuser.change_groupprofile', contest.group):
            raise PermissionDenied

        contest.contest_type = CONTEST_TYPE_ICPC
        contest.save()

        return HttpResponseRedirect(reverse("contest:contest-detail", args=[self.get_object().pk]))

    @detail_route(methods=['post'], url_path='submission/(?P<submission_id>[0-9]+)/rejudge')
    def rejudge_submission(self, request, pk=None, submission_id=None):
        submission = Submission.objects.filter(pk=submission_id)
        if len(submission) > 0:
            submission = submission[0]
        else:
            raise Http404

        if not request.user.has_perm('ojuser.change_groupprofile', submission.problem.contest.group):
            raise PermissionDenied

        submission.rejudge()

        return Response()

    @detail_route(methods=['post'], url_path='problem/(?P<problem_index>[A-Z]+)/rejudge')
    def rejudge_problem(self, request, pk=None, problem_index=None):
        problem = ContestProblem.objects.filter(contest=self.get_object(), index=problem_index)
        if len(problem) > 0:
            problem = problem[0]
        else:
            raise Http404

        if not request.user.has_perm('ojuser.change_groupprofile', problem.contest.group):
            raise PermissionDenied

        submissions = problem.contest_submissions.all()
        for submission in submissions:
            submission.rejudge()

        return Response()


class ContestListView(ListView):

    model = Contest
    paginate_by = 10

    def get_queryset(self):
        group_can_view_qs = get_objects_for_user(
            self.request.user,
            'ojuser.view_groupprofile',
            with_superuser=True
        )
        # self.contest_can_view_qs = self.request.user.contests.all()
        self.contest_can_view_qs = Contest.objects.filter(Q(group__in=group_can_view_qs)|Q(author=self.request.user))
        self.filter = ContestFilter(
            self.request.GET,
            queryset=self.contest_can_view_qs,
            user=self.request.user
        )
        return self.filter.qs

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ContestListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContestListView, self).get_context_data(**kwargs)
        contests_table = ContestTable(self.get_queryset())
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(contests_table)
        #  add filter here
        context['contests_table'] = contests_table
        context['filter'] = self.filter
        context['contests_can_view'] = self.contest_can_view_qs
        # context['contests_can_delete'] = self.contest_can_delete_qs
        # context['contests_can_change'] = self.contest_can_change_qs
        return context


class ContestCreateView(CreateView):
    template_name = 'contest/contest_create_form.html'
    success_message = "your Contest has been created successfully"
    model = Contest
    form_class = ContestForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        gid = kwargs.get('gid')
        try:
            gid = int(gid)
        except Exception as ex:
            gid = -1
        self.group = get_object_or_404(get_objects_for_user(request.user, 'ojuser.change_groupprofile', with_superuser=True), pk=gid)
        return super(ContestCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        problem_list = self.request.POST.getlist('problem_id')
        score_list = self.request.POST.getlist('problem_score_custom')
        problem_tile_list = self.request.POST.getlist('problem_title_custom')
        score_list = map(lambda x: int(x), score_list)
        problem_list = map(lambda x: int(x), problem_list)
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.lang_limited = form.cleaned_data['lang_limited']
        self.object.group = self.group
        self.object.save()
        pindex = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(len(problem_list)):
            p = Problem.objects.filter(pk=problem_list[i]).first()
            if not p or ContestProblem.objects.filter(problem=p, contest=self.object).count() > 0:
                continue
            cp = ContestProblem(problem=p, title=problem_tile_list[i],
                                score=score_list[i], contest=self.object, index=pindex[i])
            cp.save()
        return super(ContestCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContestCreateView, self).get_context_data(**kwargs)
        groups = get_objects_for_user(self.request.user, 'ojuser.change_groupprofile', with_superuser=True)
        control_problem = None
        for g in groups:
            if not control_problem:
                control_problem = g.problems.all()
            else:
                control_problem |= g.problems.all()
        context['control_problem'] = control_problem.distinct() if control_problem else None
        return context

    def get_success_url(self):
        return reverse("contest:contest-detail", args=[self.object.pk])


class ContestDetailView(DetailView):
    model = Contest

    @method_decorator(login_required)
    @method_decorator(view_permission_required)
    def dispatch(self, request, *args, **kwargs):
        # self.object = get_object_or_404(self.get_queryset(), pk=pk)
        return super(ContestDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContestDetailView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['is_admin'] = self.request.user.has_perm('ojuser.change_groupprofile', self.object.group)
        context['show_problems'] = context['is_admin'] or self.object.ended() == 0
        return context


class ProblemDetailView(DetailView):
    model = Contest
    template_name = 'contest/problem_detail.html'

    def get_queryset(self):
        return Contest.objects.all()

    @method_decorator(login_required)
    @method_decorator(view_permission_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        index = kwargs.get('index', '#')
        self.problem = ContestProblem.objects.filter(contest__pk=pk, index=index).first()
        if not self.problem:
            raise Http404

        contest = self.get_object()
        if not request.user.has_perm('ojuser.change_groupprofile', contest.group)\
            and contest.ended() != 0:
            raise PermissionDenied
        return super(ProblemDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProblemDetailView, self).get_context_data(**kwargs)
        context['problem'] = self.problem
        if self.request.user.has_perm('ojuser.change_groupprofile', self.object.group):
            context['is_admin'] = True
        return context


class SubmissionListView(ListView):
    model = Submission
    template_name = 'contest/submission_list.html'
    paginate_by = 15

    def get_queryset(self):
        queryset = None
        if self.request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            queryset = Submission.objects.filter(problem__contest=self.contest).all()
        else:
            queryset = Submission.objects.filter(problem__contest=self.contest, user=self.request.user).all()
        self.filter = SubmissionFilter(
            self.request.GET,
            queryset=queryset,
            problems=self.contest.problems.all(),
        )
        return self.filter.qs.order_by('-pk')


    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.contest = get_object_or_404(Contest.objects.filter(group__in=get_objects_for_user(
            request.user,
            'ojuser.view_groupprofile',
            with_superuser=True)), pk=pk)
        return super(SubmissionListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubmissionListView, self).get_context_data(**kwargs)
        submissions_table = SubmissionTable(self.get_queryset())
        # submissions_table.paginate(page=self.request.get('page', 1), per_page=20)
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(submissions_table)
        #  add filter here
        context['submissions_table'] = submissions_table
        # context['submissions'] = self.filter.qs.order_by('-pk')
        #  add filter here
        context['filter'] = self.filter
        context['contest'] = self.contest
        context['problems'] = self.contest.problems.all()
        if self.request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            context['is_admin'] = True
        return context


class BoardView(DetailView):
    model = Contest
    template_name = 'contest/contest_board.html'

    @method_decorator(login_required)
    @method_decorator(view_permission_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.contest = self.get_object()
        return super(BoardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)
        context['problems'] = self.object.problems.all()
        is_admin = self.request.user.has_perm('ojuser.change_groupprofile', self.contest.group)
        if is_admin:
            context['is_admin'] = True
            context['view_groups'] = self.contest.group.get_descendants(include_self=True)
            if self.object.contest_type == CONTEST_TYPE_ICPC_MANUAL:
                context['can_release'] = True
        context['force_realtime'] = '1' if self.contest.ended() == 1 and self.contest.contest_type == CONTEST_TYPE_ICPC and not is_admin else '0'
        return context


class ContestUpdateView(UpdateView):
    template_name = 'contest/contest_create_form.html'
    success_message = "your Contest has been updated successfully"
    form_class = ContestForm
    model = Contest

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.pk = pk
        return super(ContestUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("contest:contest-detail", args=[self.pk])

    def form_valid(self, form):
        problem_list = self.request.POST.getlist('problem_id')
        score_list = self.request.POST.getlist('problem_score_custom')
        problem_tile_list = self.request.POST.getlist('problem_title_custom')
        score_list = map(lambda x: int(x), score_list)
        problem_list = map(lambda x: int(x), problem_list)
        self.object = form.save(commit=False)
        self.object.lang_limited = form.cleaned_data['lang_limited']
        self.object.save()
        pindex = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        problem_pks = []
        for i in range(len(problem_list)):
            p = Problem.objects.filter(pk=problem_list[i]).first()
            cp = ContestProblem.objects.filter(contest=self.object, index=pindex[i]).first()
            if not cp:
                cp = ContestProblem()
            cp.problem = p
            cp.title = problem_tile_list[i]
            cp.score = score_list[i]
            cp.contest = self.object
            cp.index = pindex[i]
            cp.save()
            problem_pks.append(cp.pk)

        for p in self.object.problems.all():
            if p.pk not in problem_pks:
                p.delete()
        self.object.save()
        return super(ContestUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContestUpdateView, self).get_context_data(**kwargs)
        context['now'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        groups = get_objects_for_user(self.request.user, 'ojuser.change_groupprofile', with_superuser=True)
        control_problem = None
        for g in groups:
            if not control_problem:
                control_problem = g.problems.all()
            else:
                control_problem |= g.problems.all()
        context['control_problem'] = control_problem.distinct() if control_problem else None
        context['problems'] = self.object.problems.all()
        return context

    def get_form_kwargs(self):
        kwargs = super(ContestUpdateView, self).get_form_kwargs()
        d, t = self.object.get_date_time()
        kwargs['initial'] = {
            'lang_limited': self.object.lang_limited,
            'start_date': d,
            'start_time': t,
        }
        return kwargs


class SubmissionCreateView(DetailView):
    template_name = 'contest/submission_create_form.html'
    success_message = "your submission has been created successfully"
    model = Contest

    def get_queryset(self):
        return Contest.objects.all()

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.index = request.GET.get('index', None)
        self.contest = self.get_object()
        check_permission(request.user, self.contest)

        if self.contest.ended() != 0 and not request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            raise PermissionDenied

        return super(SubmissionCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubmissionCreateView, self).get_context_data(**kwargs)
        context['contest'] = self.contest
        queryset = None
        if self.index:
            queryset = ContestProblem.objects.filter(contest=self.contest, index=self.index).first()
        else:
            queryset = self.contest.problems.first()
        form = SubmissionForm(initial={'problem': queryset})
        form.set_choice(self.contest)
        context['form'] = form
        if self.request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            context['is_admin'] = True
        return context


class SubmissionDetailView(DetailView):
    model = Submission
    template_name = 'contest/submission_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, cpk=None, pk=None, *args, **kwargs):
        self.user = request.user
        self.contest = Contest.objects.filter(pk=cpk).first()
        if not self.contest:
            raise Http404()
        if self.user != self.get_object().user \
            and not request.user.has_perm("ojuser.change_groupprofile", self.contest.group):
            raise PermissionDenied
        return super(SubmissionDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        submission = self.object
        status = submission.get_status_display()
        if submission.status == 'JD':
            status = u'正在运行第' + str(len(self.object.cases)) + u'组数据'
        context = super(SubmissionDetailView, self).get_context_data(**kwargs)
        context['status'] = status
        context['contest'] = self.contest
        if self.request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            context['is_admin'] = True
        cases = submission.cases
        if submission.status == 'JD' and len(cases) < submission.problem.problem.cases.count():
            cases.append({
                'status': 'Judging',
                'position': len(cases),
                'time': 0,
                'memory': 0,
            })
        context['cases'] = cases
        return context


class NotificationListView(DetailView):

    model = Contest
    template_name = 'contest/notification_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        return super(NotificationListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)
        self.notification_can_view_qs = self.object.notifications.all()
        notifications_table = NotificationTable(self.notification_can_view_qs)
        RequestConfig(self.request).configure(notifications_table)
        context['notification_table'] = notifications_table
        if self.request.user.has_perm('ojuser.change_groupprofile', self.object.group):
            context['is_admin'] = True
        return context


class NotificationCreateView(TemplateView):

    template_name = 'contest/notification_create_form.html'
    success_message = "your notification has been created successfully"

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.contest = Contest.objects.filter(pk=pk).first()
        if not self.contest:
            raise Http404()
        if not request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            raise PermissionDenied
        return super(NotificationCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'POST':
            form = NotificationForm(request.POST)
            if form.is_valid():
                object = form.save(commit=False)
                object.contest = self.contest
                object.author = request.user
                object.save()
                return HttpResponseRedirect(reverse('contest:contest-detail', args=[self.contest.pk, ]))
        return super(NotificationCreateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(NotificationCreateView, self).get_context_data(**kwargs)
        context['form'] = NotificationForm()
        context['contest'] = self.contest
        return context


class NotificationUpdateView(TemplateView):

    template_name = 'contest/notification_create_form.html'
    success_message = "your notification has been created successfully"

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, nid=None, *args, **kwargs):
        self.contest = Contest.objects.filter(pk=pk).first()
        self.notification = Notification.objects.filter(pk=nid).first()
        if not self.contest or not self.notification:
            raise Http404()
        if not request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            raise PermissionDenied
        return super(NotificationUpdateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'POST':
            form = NotificationForm(request.POST, instance=self.notification)
            if form.is_valid():
                object = form.save()
                object.contest = self.contest
                object.author = request.user
                object.save()
                return HttpResponseRedirect(reverse('contest:notification-list', args=[self.contest.pk, ]))
        return super(NotificationUpdateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(NotificationUpdateView, self).get_context_data(**kwargs)
        context['form'] = NotificationForm(instance=self.notification)
        context['contest'] = self.contest
        return context


class ClarificationListView(ListView):

    model = Contest
    template_name = 'contest/clarification_list.html'

    paginate_by = 15

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.contest = get_object_or_404(Contest.objects.filter(group__in=get_objects_for_user(
            request.user,
            'ojuser.view_groupprofile',
            with_superuser=True)), pk=pk)
        return super(ClarificationListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClarificationListView, self).get_context_data(**kwargs)
        self.clarification_can_view_qs = self.contest.clarifications.all()
        notifications_table = ClarificationTable(self.clarification_can_view_qs)
        RequestConfig(self.request, paginate={'per_page': 20}).configure(notifications_table)
        context['clarification_table'] = notifications_table
        context['contest'] = self.contest
        if self.request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            context['is_admin'] = True
        return context


class QuestionView(CreateView):

    model = Clarification
    template_name = 'contest/add_clarification.html'
    form_class = QuestionForm
    success_message = "your question has been created successfully"

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.contest = get_object_or_404(Contest.objects.filter(group__in=get_objects_for_user(
            request.user,
            'ojuser.view_groupprofile',
            with_superuser=True)), pk=pk)
        return super(QuestionView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.contest = self.contest
        self.object.author = self.request.user
        self.object.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            self.success_message
            )
        return super(QuestionView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QuestionView, self).get_context_data()
        context['contest'] = self.contest
        context['form'] = QuestionForm()
        return context

    def get_success_url(self):
        return reverse('contest:contest-detail', args=[self.contest.pk])


class AnswerView(UpdateView):

    model = Clarification
    template_name = 'contest/add_clarification.html'
    form_class = AnswerForm

    @method_decorator(login_required)
    def dispatch(self, request, cpk=None, *args, **kwargs):
        self.contest = get_object_or_404(Contest.objects.filter(group__in=get_objects_for_user(
            request.user,
            'ojuser.change_groupprofile',
            with_superuser=True)), pk=cpk)
        return super(AnswerView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AnswerView, self).get_context_data()
        context['contest'] = self.contest
        context['form'] = self.form_class()
        return context

    def get_success_url(self):
        return reverse('contest:clarification-list', args=[self.contest.pk])


class QuestionDeleteView(DeleteView):
    model = Clarification
    template_name = 'ojuser/group_confirm_delete.html'

    @method_decorator(login_required)
    def dispatch(self, request, cpk=None, *args, **kwargs):
        self.contest = get_object_or_404(Contest.objects.filter(group__in=get_objects_for_user(
            request.user,
            'ojuser.change_groupprofile',
            with_superuser=True)), pk=cpk)
        return super(QuestionDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('contest:clarification-list', args=[self.contest.pk])


class PrinterView(DetailView):
    model = Contest
    template_name = "contest/contest_printer.html"

    @method_decorator(login_required)
    @method_decorator(view_permission_required)
    def dispatch(self, request, *args, **kwargs):
        contest = self.get_object()
        if contest is None:
            raise Http404
        if not (request.user.is_superuser or request.user.is_staff or request.user.profile.is_teacher):
            if contest.ended() != 0:
                raise Http404
        return super(PrinterView, self).dispatch(request, *args, **kwargs)

    def obfuse_auth_info(self, text):
        if len(text) & 1 != 0:
            text = "\0" + text
        result = []
        for i in xrange(0, len(text), 2):
            l = ord(text[i])
            r = ord(text[i + 1])
            l ^= r
            r ^= ~l & 0xff
            result.append(chr(l))
            result.append(chr(r))
        return base64.encodestring(''.join(result))

    def get_context_data(self, **kwargs):
        context = super(PrinterView, self).get_context_data()

        if 'success' in self.request.GET:
            context['success'] = True
        else:
            context['auth'] = self.obfuse_auth_info(u"{}|{}".format(self.request.user.username, self.request.user.profile.nickname).encode('utf8'))
        return context