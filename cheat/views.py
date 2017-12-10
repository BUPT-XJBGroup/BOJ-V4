from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from contest.models import Contest
from django.http import Http404, HttpResponseForbidden

from .models import Record, RecordFilter, RecordTable

from guardian.shortcuts import get_objects_for_user
from common.perm import change_permission_required
from django_tables2 import RequestConfig
import logging
logger = logging.getLogger('django')
# Create your views here.

class RecordListView(ListView):

    model = Record
    paginate_by = 10

    def get_queryset(self):
        queryset = Record.objects.filter(problem__contest=self.contest)
        self.filter = RecordFilter(
            self.request.GET,
            queryset=queryset,
        )
        self.filter.filters.get('problem').queryset = self.contest.problems.all()
        return self.filter.qs.order_by('-probability')

    @method_decorator(login_required)
    @method_decorator(change_permission_required)
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.contest = Contest.objects.get(pk=pk)
        return super(RecordListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RecordListView, self).get_context_data(**kwargs)
        contests_table = RecordTable(self.get_queryset())
        RequestConfig(self.request, paginate={'per_page': self.paginate_by}).configure(contests_table)
        #  add filter here
        context['records_table'] = contests_table
        context['filter'] = self.filter
        context['contest'] = self.contest
        return context


class RecordDetailView(DetailView):

    model = Record

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.user = request.user
        group = self.get_object().problem.contest.group
        if not group or not request.user.has_perm("ojuser.view_groupprofile", group):
            raise Http404("Submission does not exist")
        return super(RecordDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RecordDetailView, self).get_context_data(**kwargs)
        context['code1'] = self.get_object().sub1.code
        context['code2'] = self.get_object().sub2.code
        return context

