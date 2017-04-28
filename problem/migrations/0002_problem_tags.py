# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.TextField(default='None'),
        ),
    ]
