from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from contest.models import Contest

from .models import Record, RecordFilter, RecordTable

from guardian.shortcuts import get_objects_for_user
from common.perm import change_permission_required
from django_tables2 import RequestConfig
# Create your views here.

class RecordListView(ListView):

    model = Record
    paginate_by = 10

    def get_queryset(self):
        self.qs = reduce(lambda x, y: x.cheat.all() | y.cheat.all(), self.contest.problems.all())
        #for g in self.contest.problems.all():
        #    self.qs |= g.cheat.all()
        self.filter = RecordFilter(
            self.request.GET,
            queryset=self.qs,
        )
        self.filter.filters.get('problem').queryset = self.contest.problems.all()
        return self.filter.qs

    @method_decorator(login_required)
    @method_decorator(change_permission_required)
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.contest = Contest.objects.get(pk=pk)
        return super(RecordListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RecordListView, self).get_context_data(**kwargs)
        contests_table = RecordTable(self.get_queryset())
        RequestConfig(self.request).configure(contests_table)
        #  add filter here
        context['records_table'] = contests_table
        context['filter'] = self.filter
        context['contest'] = self.contest
        return context


class RecordDetailView(DetailView):

    model = Record
