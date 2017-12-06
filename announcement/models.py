from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Announcement(models.Model):
    title = models.CharField(max_length=128, default='Untitled')
    content = models.TextField(default=None)
    author = models.ForeignKey(User, related_name='created_announcements')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_sticky = models.BooleanField(default=False)

    last_update_user = models.ForeignKey(User, related_name=None)

    def __unicode__(self):
        return self.title

