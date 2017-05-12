from django import forms

class GetCodeForm(forms.Form):
    code_a = forms.CharField(widget = forms.Textarea)
    code_b = forms.CharField(widget = forms.Textarea)
