#encoding: utf-8
import django_tables2 as tables
from .models import Problem
from django_tables2.utils import A


class ProblemTable(tables.Table):
    title = tables.LinkColumn('problem:problem-detail', args=[A('pk')], verbose_name=u"题目名称")
    status = tables.TemplateColumn(
        template_name='problem/problem_list_external.html',
        orderable=False,
        verbose_name=u"运行结果"
    )

    class Meta:
        model = Problem
        fields = ('id', 'title', 'time_limit', 'memory_limit', 'superadmin', 'status',)
        template = 'django_tables2/bootstrap.html'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProblemTable, self).__init__(*args, **kwargs)
        self.base_columns['time_limit'].verbose_name=u"运行时间限制"
        self.base_columns['memory_limit'].verbose_name=u"运行内存限制"
        self.base_columns['status'].verbose_name=u"操作"


