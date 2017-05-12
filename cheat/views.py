#encoding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from multiprocessing import Pool
import os, time, random, sys, Queue
from multiprocessing.managers import BaseManager
from .forms import GetCodeForm
from .models import CheatMethod
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

'''
class GetCodeView(FormView):
    template_name = "cheat.html"
    form_class = GetCodeForm
    form_class.code_a = "hahahh"
    success_url = '/cheat'
    
    def form_valid(self, form):
        code_a = form.cleaned_data['code_a']
        code_b = form.cleaned_data['code_b']
        print (code_a, code_b)
        CheckCheat.antiCheat(code_a, code_b)
        return super(GetCodeView, self).form_valid(form)
'''


class CheatTestView(TemplateView):
    template_name = "cheat/cheat_echarts.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CheatTestView, self).dispatch(request, *args, **kwargs)


'''
class CheatStartView(TemplateView):
    template_name = "cheat.html"

    def get_context_data(self, **kwargs):
        context = super(CheatStartView, self).get_context_data(**kwargs)
        context['code_a'] = "The last version of Hahah" 
        print (context['code_a'], " ----- ")
        return context
'''
