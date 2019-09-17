#encoding: utf-8
import django_filters
from django_filters.widgets import BooleanWidget, CSVWidget
from .models import Problem, ProblemTag
from ojuser.models import GroupProfile
from guardian.shortcuts import get_objects_for_user
from django_select2.forms import ModelSelect2MultipleWidget
from django_select2.forms import ModelSelect2Widget
#  from guardian.shortcuts import get_objects_for_user


class ProblemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label=u"题目名称")
    tags = django_filters.ModelChoiceFilter(queryset=ProblemTag.objects.all(), label=u"标签")
    groups = django_filters.ModelChoiceFilter(queryset=GroupProfile.objects.all(), label=u"用户组")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProblemFilter, self).__init__(*args, **kwargs)
        self.filters.get('groups').queryset=get_objects_for_user(self.user, 'ojuser.view_groupprofile', with_superuser=True)

    class Meta:
        model = Problem
        fields = ['title', 'groups', ]

