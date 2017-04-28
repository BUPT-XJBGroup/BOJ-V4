import django_tables2 as tables
from .models import Problem
from django_tables2.utils import A


class ProblemTable(tables.Table):
    pk = tables.LinkColumn(accessor='pk', verbose_name="id")
    title = tables.LinkColumn('problem:problem-detail', args=[A('pk')], verbose_name="Problem Title")
    superadmin = tables.LinkColumn(accessor='superadmin', verbose_name="Creator")
    status = tables.TemplateColumn(
        template_name='problem/problem_list_external.html',
        orderable=False,
        verbose_name = "Operations"
    )

    class Meta:
        model = Problem
        order_by = ['pk']
        fields = ('pk', 'title', 'superadmin', 'status',)
        template = 'django_tables2/bootstrap.html'

"""
class ProblemCreateTable(tables.Table):
    name = tables.LinkColumn('mygroup-detail', args=[A('pk')], verbose_name="Group")
    nickname = tables.Column(accessor='nickname', verbose_name="Nickname")
    superadmin = tables.Column(accessor='superadmin', verbose_name="Creater")
    desc = tables.TemplateColumn(
        '{{ record.desc|truncatechars:25 }}',
        verbose_name="Description",
        orderable=False,
    )
    status = tables.TemplateColumn(
        template_name='ojuser/group_list_external.html',
        orderable=False,
        verbose_name='Operator',
    )

    class Meta:
        model = Problem
        fields = ('table', 'nickname', 'superadmin', 'desc', 'status',)
        template = 'django_tables2/bootstrap.html'
"""

class SubmissionTable(tables.Table):

    class Meta:
        model = Problem
        fields = ()
        template = 'django_tables2/bootstrap.html'