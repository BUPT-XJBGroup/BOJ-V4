# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0007_auto_20170624_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='info',
            field=models.TextField(default=b''),
        ),
    ]
