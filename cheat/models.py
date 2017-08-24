from django.db import models
import django_filters
import django_tables2 as tables
from contest.models import Contest, Notification, Clarification, ContestSubmission, ContestProblem
from django_tables2.utils import A

# Create your models here.


class Record(models.Model):

    problem = models.ForeignKey(ContestProblem, related_name='cheat')
    sub1 = models.ForeignKey(ContestSubmission, related_name="record1")
    sub2 = models.ForeignKey(ContestSubmission, related_name="record2")
    probability = models.FloatField(default=0.0, db_index=True)
    user1 = models.CharField(max_length='32', default='', db_index=True)
    user2 = models.CharField(max_length='32', default='', db_index=True)


class RecordFilter(django_filters.FilterSet):
    problem = django_filters.ModelChoiceFilter(queryset=ContestProblem.objects.all())
    author = django_filters.CharFilter(method='filter_author', label='author')
    submission = django_filters.CharFilter(method='filter_submission', label='submission')
    probability = django_filters.NumericRangeFilter()

    def filter_author(self, queryset, name, value):
        return queryset.filter(user1__icontains=value) | queryset.filter(user2__icontains=value)

    def filter_submission(self, queryset, name, value):
        return queryset.filter(sub1_id=value) | queryset.filter(sub2_id=value)

    class Meta:
        model = Record
        fields = ['problem', 'author', 'submission', 'probability']


class RecordTable(tables.Table):
    problem = tables.LinkColumn('contest:problem-detail', args=[A('problem.contest.pk'), A('problem.index')], accessor='problem.index')
    sub1 = tables.LinkColumn('contest:submission-detail', args=[A('problem.contest.pk'), A('sub1.pk'), ], accessor='sub1.pk')
    user1 = tables.Column()
    sub2 = tables.LinkColumn('contest:submission-detail', args=[A('problem.contest.pk'), A('sub2.pk')], accessor='sub2.pk')
    user2 = tables.Column()
    probability = tables.LinkColumn('cheat:record-detail', args=[A('problem.contest.pk'), A('pk')])

    class Meta:
        model = Record
        fields = ('problem', 'sub1', 'user1', 'sub2', 'user2', 'probability')
        template = 'django_tables2/bootstrap.html'

