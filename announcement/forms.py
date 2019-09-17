# encoding: utf8

from django.db import models
from django.forms import ModelForm
from .models import Announcement

class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        exclude = ['update_time', 'create_time', 'author', 'last_update_user']
        labels = {
            'title' : "标题",
            'content' : "正文",
            'is_sticky' : "置顶"
        }
