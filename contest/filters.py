#encoding: utf-8
import django_filters
from django_filters.widgets import BooleanWidget
from .models import Contest, ContestSubmission
from django.contrib.auth.models import User
from ojuser.models import GroupProfile
from guardian.shortcuts import get_objects_for_user
from bojv4.conf import LANGUAGE, STATUS_CODE
#  from guardian.shortcuts import get_objects_for_user


class SubmissionFilter(django_filters.FilterSet):

    pk = django_filters.CharFilter(name='id', label='id')
    submission__language = django_filters.ChoiceFilter(choices=LANGUAGE.choice(), label=u'语言')
    problem = django_filters.ModelChoiceFilter(queryset=(('A', 'A'),), label=u'题目')
    submission__status = django_filters.ChoiceFilter(choices=STATUS_CODE.choice(), label='状态')
    submission__user = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label=u'用户')

    def __init__(self, *args, **kwargs):
        self.problems = kwargs.pop('problems')
        self.users = kwargs.pop('users')
        super(SubmissionFilter, self).__init__(*args, **kwargs)
        self.filters.get('problem').queryset=self.problems
        self.filters.get('submission__user').queryset=self.users


    class Meta:
        model = ContestSubmission
        fields = ['pk', 'problem', 'submission__language', 'submission__status']
        order_by = 'desc'


def view_groups(request):
    queryset = get_objects_for_user(
                    request.user,
                    'ojuser.view_groupprofile',
                    with_superuser=True
                ).distinct().all()
    return queryset


class ContestFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label=u'考试名称')
    group = django_filters.ModelChoiceFilter(queryset=GroupProfile.objects.all(), label=u'所属用户组')
    can_manage = django_filters.BooleanFilter(method='filter_can_manage', label=u'是否可以管理', widget=BooleanWidget())

    def filter_can_manage(self, queryset, name, value):
        groups = get_objects_for_user(
            self.user,
            'ojuser.change_groupprofile',
            with_superuser=True
        ).distinct()
        if value:
            return queryset.filter(pk__in=groups)
        else:
            return queryset.exclude(pk__in=groups)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ContestFilter, self).__init__(*args, **kwargs)
        self.filters.get('group').queryset = get_objects_for_user(self.user, 'ojuser.view_groupprofile', with_superuser=True)


    class Meta:
        model = Contest
        fields = ['name', 'group', 'can_manage', ]


