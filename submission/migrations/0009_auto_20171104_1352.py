# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0008_auto_20171002_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caseresult',
            name='status',
            field=models.CharField(default=b'QUE', max_length=3, choices=[(b'PD', '\u63d0\u4ea4\u4e2d'), (b'SE', '\u7cfb\u7edf\u9519\u8bef'), (b'CL', '\u7f16\u8bd1\u4e2d'), (b'CE', '\u7f16\u8bd1\u9519\u8bef'), (b'JD', '\u7a0b\u5e8f\u8fd0\u884c\u4e2d'), (b'AC', '\u901a\u8fc7'), (b'PE', '\u683c\u5f0f\u9519\u8bef'), (b'IR', b'Invalid Return'), (b'WA', '\u7b54\u6848\u9519\u8bef'), (b'RE', '\u8fd0\u884c\u65f6\u9519\u8bef'), (b'TLE', '\u8fd0\u884c\u8d85\u65f6'), (b'MLE', '\u5185\u5b58\u4f7f\u7528\u8d85\u8fc7\u9650\u5236'), (b'OLE', '\u8f93\u51fa\u957f\u5ea6\u8d85\u8fc7\u9650\u5236'), (b'IE', b'Internal Error')]),
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(default=b'QUE', max_length=3, choices=[(b'PD', '\u63d0\u4ea4\u4e2d'), (b'SE', '\u7cfb\u7edf\u9519\u8bef'), (b'CL', '\u7f16\u8bd1\u4e2d'), (b'CE', '\u7f16\u8bd1\u9519\u8bef'), (b'JD', '\u7a0b\u5e8f\u8fd0\u884c\u4e2d'), (b'AC', '\u901a\u8fc7'), (b'PE', '\u683c\u5f0f\u9519\u8bef'), (b'IR', b'Invalid Return'), (b'WA', '\u7b54\u6848\u9519\u8bef'), (b'RE', '\u8fd0\u884c\u65f6\u9519\u8bef'), (b'TLE', '\u8fd0\u884c\u8d85\u65f6'), (b'MLE', '\u5185\u5b58\u4f7f\u7528\u8d85\u8fc7\u9650\u5236'), (b'OLE', '\u8f93\u51fa\u957f\u5ea6\u8d85\u8fc7\u9650\u5236'), (b'IE', b'Internal Error')]),
        ),
    ]
