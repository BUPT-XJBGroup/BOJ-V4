#encoding: utf-8
from django import forms
from .models import Submission
from bojv4.conf import LANGUAGE
from django_select2.forms import ModelSelect2Widget


class SubmissionForm(forms.ModelForm):

    language = forms.ChoiceField(choices=LANGUAGE.choice(), widget=forms.Select())
    code = forms.CharField(max_length=65535, widget=forms.Textarea)

    class Meta:
        model = Submission
        fields = ('code', 'language')

    def __init__(self, qs=None, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
        self.fields['code'].label=u'代码'
        self.fields['language'].label=u'程序语言'
