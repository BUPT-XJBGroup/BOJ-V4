#encoding: utf-8
from django import forms
from django_select2.forms import ModelSelect2MultipleWidget
#  from django.contrib.auth.models import Group
from .models import Problem, ProblemTag
from ojuser.models import GroupProfile


class ProblemForm(forms.ModelForm):

    is_spj = forms.NullBooleanField(widget=forms.CheckboxInput(), initial=False)
    tags = forms.ModelMultipleChoiceField(required=False, queryset=ProblemTag.objects.all(),
        widget=ModelSelect2MultipleWidget(
                 search_fields=[
                    'name__icontains',
                    'nickname__icontains',
                ]))

    class Meta:
        model = Problem
        exclude = ["superadmin", "is_checked", "created_time", "last_updated_time", "desc",
                "code_length_limit"]
        widgets = {
            'groups': ModelSelect2MultipleWidget(
                search_fields=[
                    'name__icontains',
                    'nickname__icontains',
                ]
            ),
            'tags': ModelSelect2MultipleWidget(
                search_fields=[
                    'name__icontains'
                ]
            )
        }

    def __init__(self, *args, **kwargs):
        super(ProblemForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = u"题目"
        self.fields['time_limit'].label = u"运行时间限制"
        self.fields['memory_limit'].label = u"运行时间限制"
        self.fields['groups'].label = u"所属用户组"

