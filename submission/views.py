from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from bojv4.conf import LANGUAGE

from .abstract_models import NormalSubmission as Submission
from .forms import SubmissionForm
from .serializers import SubmissionSerializer
from .tables import SubmissionTable
from .filters import SubmissionFilter

from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import Http404, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import EmptyQuerySet
from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user
from django_tables2 import RequestConfig

from problem.models import Problem
from ojuser.models import GroupProfile
import logging
logger = logging.getLogger('django')
#  from guardian.shortcuts import get_objects_for_user


class CaseResultPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return obj.submission.problem.view_by_user(user=request.user)


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated,)


class SubmissionListView(ListView):

    model = Submission
    paginate_by = 15
    template_name = 'submission/submission_list.html'

    def get_queryset(self):
        groups = get_objects_for_user(self.user, 'ojuser.view_groupprofile', GroupProfile)
        res = Problem.objects.filter(groups__in=groups).all()
        ans = Submission.objects.filter(problem__groups__in=groups).order_by('-pk')
        self.filter = SubmissionFilter(
            self.request.GET,
            queryset=ans,
            problems=res
        )
        return self.filter.qs

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(SubmissionListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubmissionListView, self).get_context_data(**kwargs)
        submissions_table = SubmissionTable(self.get_queryset())
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(submissions_table)
        #  add filter here
        context['submissions_table'] = submissions_table
        #  add filter here
        context['filter'] = self.filter
        return context


class SubmissionDetailView(DetailView):

    model = Submission
    template_name = 'submission/submission_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.user = request.user
        problem = self.get_object().problem
        if not problem or not problem.view_by_user(request.user):
            raise PermissionDenied
        try:
            csub = self.get_object().contest_submission
            raise PermissionDenied
        except:
            pass
        return super(SubmissionDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        logger.warning('============test===============')
        status = self.object.get_status_display()
        context = super(SubmissionDetailView, self).get_context_data(**kwargs)
        context['status'] = status
        ce = self.object.get_info('compile-message')
        context['compile_message'] = ce
        cases = self.object.cases
        if self.object.status == 'JD' and len(cases) < self.object.problem.cases.count():
            cases.append({
                'status': 'Judging',
                'position': len(cases),
                'time': 0,
                'memory': 0,
            })
        context['cases'] = cases
        return context


class SubmissionCreateView(SuccessMessageMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'submission/submission_create_form.html'
    success_message = "your submission has been created successfully"

    @method_decorator(login_required)
    def dispatch(self, request, pid=None, *args, **kwargs):
        pid = self.kwargs['pid']
        self.problem = Problem.objects.filter(pk=pid).first()
        if not self.problem or not self.problem.view_by_user(request.user):
            raise PermissionDenied
        if not self.problem.is_checked:
            return HttpResponseForbidden()
        self.user = request.user
        return super(SubmissionCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kw = super(SubmissionCreateView, self).get_form_kwargs()
        kw['qs'] = LANGUAGE.choice()
        return kw

    def get_context_data(self, **kwargs):
        context = super(SubmissionCreateView, self).get_context_data(**kwargs)
        context['problem'] = self.problem
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.problem = self.problem
        self.object.user = self.request.user
        self.object.save()
        # self.object.code_file.write(str(self.object.pk), i
        self.object.judge(form.cleaned_data['code'])
        return super(SubmissionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('submission:submission-list')


