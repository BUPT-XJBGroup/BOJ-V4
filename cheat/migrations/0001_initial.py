# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0010_auto_20170509_0013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('probability', models.FloatField(default=0.0, db_index=True)),
                ('user1', models.CharField(default=b'', max_length=b'32', db_index=True)),
                ('user2', models.CharField(default=b'', max_length=b'32', db_index=True)),
                ('problem', models.ForeignKey(related_name='cheat', to='contest.ContestProblem')),
                ('sub1', models.ForeignKey(related_name='record1', to='contest.ContestSubmission')),
                ('sub2', models.ForeignKey(related_name='record2', to='contest.ContestSubmission')),
            ],
        ),
    ]
