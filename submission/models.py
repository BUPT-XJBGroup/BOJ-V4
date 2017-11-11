from django.db import models
from django.contrib.auth.models import User
from problem.models import Problem
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save
from django.dispatch import receiver
from bojv4 import conf
from common.nsq_client import send_to_nsq
import json
import logging
logger = logging.getLogger('django')


class Submission(models.Model):
    CODE_LENGTH_LIMIT = 65536

    user = models.ForeignKey(User, related_name='submissions')
    problem = models.ForeignKey(Problem, related_name='submissions')
    create_time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=3, default="QUE", choices=conf.STATUS_CODE.choice())
    running_time = models.IntegerField(default=0)
    running_memory = models.IntegerField(default=0)
    info = models.TextField(default='')
    # code = models.TextField(default='')
    length = models.IntegerField(default=0)
    language = models.CharField(max_length=10, default='gcc', choices=conf.LANGUAGE.choice())
    code_file = models.FileField(null=True, upload_to='code/')

    def __init__(self, *args, **kwargs):
        super(Submission, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return str(self.pk)
        #  return "-".join([str(self.pk), str(self.user), str(self.problem), str(self.datetime)])

    def get_absolute_url(self):
        return reverse('submission:submission-detail', kwargs={'pk': self.pk})

    def get_status_display(self):
        if self.status == 'JD':
            return 'Judging in ' + str(self.cases.count()) + 'th case'
        return conf.STATUS_CODE.get_display_name(self.status)

    def set_info(self, key, value):
        try:
            _info = json.loads(self.info)
        except Exception as ex:
            _info = {}
            print ex
        _info[key] = value
        self.info = json.dumps(_info)
        print self.info

    def get_info(self, key):
        try:
            _info = json.loads(self.info)
        except Exception as ex:
            print "ex============="
            _info = {}
            print ex
        return _info.get(key, None)

    def deal_case_result(self, case):
        if case.status == 'AC' and case.position < self.problem.cases.count() - 1:
            return
        self.status = case.status
        for c in self.cases.all():
            self.running_time = max(self.running_time, c.running_time)
            self.running_memory = max(self.running_memory, c.running_memory)
        self.save()

    @property
    def code(self):
        return self.code_file.file

    def judge(self, code):
        req = {
            'grader': 'custom',
            'submission_id': self.id,
            'problem_id': self.problem.id,
            'source': code,
            'language': self.language,
            'time_limit': self.problem.time_limit / 1000.0,
            'memory_limit': self.problem.memory_limit,
            'problem_data': self.problem.get_problem_data()
        }
        
        # Temporary special time limit mercy (?) for java
        if self.language == 'JAVA8':
            req['time_limit'] *= 2

        self.score = 0
        self.status = 'PD'
        self.save()
        self.code_file.save(str(self.pk), ContentFile(code))
        logger.warning("start pending judge for submission")
        resp = send_to_nsq('judge', json.dumps(req))
        if resp.get('code', None) == -1:
            self.status = 'SE'
            self.save()
            logger.warning("result of pending judge for submission is False, message is " + resp.get('msg'))
        else:
            logger.warning("result of pending judge for submission is True, " + resp.get('msg'))
            print "Success"

    def rejudge(self):
        for c in self.cases.all():
            c.delete()
        self.judge()

    def get_code(self):
        return self.code_file.file.read()


class CaseResult(models.Model):
    submission = models.ForeignKey(Submission, related_name='cases')
    running_time = models.IntegerField(default=0)
    running_memory = models.IntegerField(default=0)
    status = models.CharField(max_length=3, default="QUE", choices=conf.STATUS_CODE.choice())
    position = models.IntegerField()
    output = models.CharField(max_length=128, default=0)


class TestCase(models.Model):

    code_file = models.FileField(null=True, upload_to='code/')
