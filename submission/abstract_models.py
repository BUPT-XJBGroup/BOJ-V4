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
import copy
logger = logging.getLogger('django')


class AbstractSubmission(models.Model):
    CODE_LENGTH_LIMIT = 65536

    create_time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=3, default="QUE", choices=conf.STATUS_CODE.choice())
    running_time = models.IntegerField(default=0)
    running_memory = models.IntegerField(default=0)
    info = models.TextField(default='')
    length = models.IntegerField(default=0)
    language = models.CharField(max_length=10, default='gcc', choices=conf.LANGUAGE.choice())
    code_file = models.FileField(null=True, upload_to='code/')

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(AbstractSubmission, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse('submission:submission-detail', kwargs={'pk': self.pk})

    def get_status_display(self):
        if self.status == 'JD':
            return 'Judging in ' + str(len(self.cases)) + 'th case'
        return conf.STATUS_CODE.get_display_name(self.status)

    def set_info(self, key, value):
        if not hasattr(self, '_info'):
            try:
                self._info = json.loads(self.info)
            except Exception as ex:
                self._info = {}
                print ex
        self._info[key] = value
        self.info = json.dumps(self._info)

    def get_info(self, key, default = None):
        if not hasattr(self, '_info'):
            try:
                self._info = json.loads(self.info)
            except Exception as ex:
                self._info = {}
                logger.error("info parameter error: %s", ex)
        return self._info.get(key, default)

    @property
    def cases(self):
        return copy.deepcopy(self.get_info('cases', []))

    def get_problem(self):
        raise Exception("no implement error")

    def add_score(self, score):
        raise Exception("no implement error")

    def deal_case_result(self, case):
        if case['status'] == 'AC' and case['position'] < self.get_problem().cases.count() - 1:
            return
        cases = self.cases
        self.status = case['status']
        for c in cases:
            self.running_time = max(self.running_time, c['time'])
            self.running_memory = max(self.running_memory, c['memory'])
        self.save()

    @property
    def code(self):
        return self.code_file.file.read()

    def get_id(self):
        return "None"

    def get_submission_type():
        return "default"

    def judge(self, code):
        problem = self.get_problem()
        req = {
            'grader': 'custom',
            'submission_id': self.get_id(),
            'submission_type': self.get_submission_type(),
            'problem_id': problem.id,
            'source': code,
            'language': self.language,
            'time_limit': problem.time_limit / 1000.0,
            'memory_limit': problem.memory_limit,
            'problem_data': problem.get_problem_data()
        }

        # Temporary special time limit mercy (?) for java
        # TODO: Remove this
        if self.language == 'JAVA8':
            req['time_limit'] *= 2

        self.score = 0
        self.status = 'PD'
        self.code_file.save(self.get_submission_type() + "-" + str(self.get_id()), ContentFile(code))
        logger.warning("start pending judge for submission")
        resp = send_to_nsq('judge', json.dumps(req))
        if resp.get('code', None) == -1:
            self.status = 'SE'
            logger.warning("result of pending judge for submission is False, message is " + resp.get('msg'))
        else:
            logger.warning("result of pending judge for submission is True, " + resp.get('msg'))
        self.save()

    def rejudge(self):
        self.set_info('cases', [])
        self.judge()

    def add_case(self, case):
        cases = self.get_info('cases', [])
        cases.append(case)
        self.set_info('cases', cases)
        self.save()


class NormalSubmission(AbstractSubmission):

    problem = models.ForeignKey(Problem, related_name='submission')
    user = models.ForeignKey(User, related_name='normal_submissions')

    def get_problem(self):
        return self.problem

    class Meta:
        db_table = 'submission'

    def add_score(self, position):
        self.score += self.problem.get_score(position)

    def get_submission_type(self):
        return "normal"

    def get_id(self):
        return self.pk

