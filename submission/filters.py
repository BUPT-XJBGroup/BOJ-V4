#encoding: utf-8
import django_filters
from django_filters.widgets import LookupTypeWidget
from .abstract_models import NormalSubmission as Submission
from problem.models import Problem
from guardian.shortcuts import get_objects_for_user

from bojv4.conf import LANGUAGE, STATUS_CODE


class SubmissionFilter(django_filters.FilterSet):

    pk = django_filters.CharFilter(name='id', label='id')
    language = django_filters.ChoiceFilter(choices=LANGUAGE.choice(), label=u"运行语言")
    problem = django_filters.ModelChoiceFilter(queryset=Problem.objects.all(), label=u"题目")
    status = django_filters.ChoiceFilter(choices=STATUS_CODE.choice(), label=u"运行结果")

    def __init__(self, *args, **kwargs):
        self.problems = kwargs.pop('problems')
        super(SubmissionFilter, self).__init__(*args, **kwargs)
        self.filters.get('problem').queryset=self.problems


    class Meta:
        model = Submission
        fields = ['pk', 'problem', 'language', 'status']
        order_by = 'desc'

