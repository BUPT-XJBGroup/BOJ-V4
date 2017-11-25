from django.shortcuts import render
from django.views.generic import TemplateView, FormView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from .models import Announcement
from .forms import AnnouncementForm
from django.shortcuts import redirect
from django.shortcuts import resolve_url


class AnnouncementListView(TemplateView):
    template_name = "announcement/announcement_list.html"

    def get_context_data(self, **kwargs):
        context = super(AnnouncementListView, self).get_context_data(**kwargs)
        announcements = Announcement.objects.order_by('-is_sticky', '-update_time').all()
        context['announcements'] = announcements
        return context


class AnnouncementView(TemplateView):
    template_name = "announcement/announcement.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super(AnnouncementView, self).get_context_data(**kwargs)
        context['announcement'] = Announcement.objects.get(pk=pk)
        context['pk'] = pk
        return context


# TODO: Fix this rubbish implementation....

class AnnouncementAddView(FormView):
    template_name = "announcement/announcement_edit.html"
    form_class = AnnouncementForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(AnnouncementAddView, self).dispatch(request, *args, **kwargs)
        return HttpResponse(status=403)

    def get_context_data(self, **kwargs):
        return super(AnnouncementAddView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        announcement = Announcement()
        announcement.title = form.cleaned_data['title']
        announcement.content = form.cleaned_data['content']
        announcement.is_sticky = form.cleaned_data['is_sticky']
        announcement.author = self.request.user
        announcement.last_update_user = self.request.user
        announcement.save()
        return redirect(resolve_url('announcement:view', pk=announcement.pk))


class AnnouncementUpdateView(UpdateView):
    template_name = "announcement/announcement_edit.html"
    # form_class = AnnouncementForm
    model = Announcement
    fields = ['title', 'content', 'is_sticky']
    success_url = ".."

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(AnnouncementUpdateView, self).dispatch(request, *args, **kwargs)
        return HttpResponse(status=403)

    # def get_context_data(self, **kwargs):
    #     return super(AnnouncementUpdateView, self).get_context_data(**kwargs)
    #
    # def form_valid(self, form):
    #     announcement = Announcement.objects.get(pk=int(self.kwargs['pk']))
    #     announcement.title = form.cleaned_data['title']
    #     announcement.content = form.cleaned_data['content']
    #     announcement.is_sticky = form.cleaned_data['is_sticky']
    #     announcement.last_update_user = self.request.user
    #     announcement.save()
    #     return redirect(resolve_url('announcement:view', pk=announcement.pk))


class AnnouncementDeleteView(DeleteView):
    template_name = "announcement/announcement_delete.html"
    model=Announcement
    success_url = resolve_url('../..')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super(AnnouncementDeleteView, self).dispatch(request, *args, **kwargs)
        return HttpResponse(status=403)

