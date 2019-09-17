# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Untitled', max_length=128)),
                ('content', models.TextField(default=None)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('is_sticky', models.BooleanField(default=False)),
                ('author', models.ForeignKey(related_name='created_announcements', to=settings.AUTH_USER_MODEL)),
                ('last_update_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
