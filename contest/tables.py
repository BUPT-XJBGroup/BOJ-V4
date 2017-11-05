# encoding: utf-8
import django_tables2 as tables
from .models import Contest, Notification, Clarification, ContestSubmission
from django_tables2.utils import A


class ContestTable(tables.Table):
    title = tables.LinkColumn('contest:contest-detail', args=[A('pk')], verbose_name=u"考试名称")
    group = tables.LinkColumn('mygroup-detail', args=[A('group.pk')], verbose_name=u"用户组")

    class Meta:
        model = Contest
        fields = ('title', 'author', 'group', 'start_time')
        template = 'django_tables2/bootstrap.html'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ContestTable, self).__init__(*args, **kwargs)
        self.base_columns['author'].verbose_name=u"管理老师"
        self.base_columns['start_time'].verbose_name=u"开始时间"




class NotificationTable(tables.Table):

    status = tables.TemplateColumn(
        template_name="contest/notification_list_external.html",
        orderable=False,
        verbose_name='Operator',
    )

    class Meta:
        model = Notification
        fields = ('title', 'content', 'create_time', 'status')
        template = 'django_tables2/bootstrap.html'


class ClarificationTable(tables.Table):

    status = tables.TemplateColumn(
        template_name="contest/clarification_list_external.html",
        orderable=False,
        verbose_name='Operator',
    )

    class Meta:
        model = Clarification
        fields = ('author', 'question', 'answer', 'status')
        template = 'django_tables2/bootstrap.html'


class SubmissionTable(tables.Table):
    pk = tables.LinkColumn('contest:submission-detail', args=[A('problem.contest.pk'), A('pk')], verbose_name='id')
    problem = tables.LinkColumn('contest:problem-detail', args=[A('problem.contest.pk'),
        A('problem.index')], verbose_name=u"题目")
    status = tables.Column(accessor='submission.status', verbose_name=u"运行结果")
    running_time = tables.Column(accessor='submission.running_time', verbose_name=u"运行时间")
    running_memory = tables.Column(accessor='submission.running_memory', verbose_name=u"内存使用")
    language = tables.Column(accessor='submission.language', verbose_name=u"程序语言")
    user = tables.Column(accessor='submission.user', verbose_name=u"提交用户")
    create_time = tables.DateTimeColumn(accessor='submission.create_time', verbose_name=u"创建时间")

    class Meta:
        model = ContestSubmission
        fields = ('pk', 'problem', 'status', 'running_time', 'running_memory', 'language',
                  'user', 'create_time')
        template = 'django_tables2/bootstrap.html'
