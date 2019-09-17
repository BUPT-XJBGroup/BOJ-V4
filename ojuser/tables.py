#encoding: utf-8
import django_tables2 as tables
from django_tables2.utils import A
from django.contrib.auth.models import User
from .models import GroupProfile


class GroupTable(tables.Table):
    name = tables.LinkColumn('mygroup-detail', args=[A('pk')], verbose_name=u"用户组")
    nickname = tables.Column(accessor='nickname', verbose_name=u"用户组昵称")
    superadmin = tables.Column(accessor='superadmin', verbose_name=u"创建者")
    desc = tables.TemplateColumn(
        '{{ record.desc|truncatechars:25 }}',
        verbose_name=u"描述",
        orderable=False,
    )
    status = tables.TemplateColumn(
        template_name='ojuser/group_list_external.html',
        orderable=False,
        verbose_name=u'操作',
    )

    class Meta:
        model = GroupProfile
        order_by = ['name']
        fields = ('name', 'nickname', 'superadmin', 'desc', 'status',)
        template = 'django_tables2/bootstrap.html'


class GroupUserTable(tables.Table):
    status = tables.TemplateColumn(
        template_name='ojuser/group_user_external.html',
        orderable=False,
        verbose_name=u'操作',
    )

    class Meta:
        model = User
        fields = ('username', 'email', )
        template = 'django_tables2/bootstrap.html'
