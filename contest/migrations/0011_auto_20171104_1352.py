# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0010_auto_20170509_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestsubmission',
            name='submission',
            field=models.OneToOneField(related_name='contest_submissions', to='submission.Submission'),
        ),
    ]
