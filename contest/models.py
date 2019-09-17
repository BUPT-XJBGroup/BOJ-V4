from django.db import models
from django.contrib.auth.models import User
from ojuser.models import GroupProfile
from submission.abstract_models import AbstractSubmission
from problem.models import Problem
from bojv4 import conf
import time
from datetime import datetime, timedelta
# Create your models here.


class Contest(models.Model):

    author = models.ForeignKey(User, related_name='contests')
    group = models.ForeignKey(GroupProfile, related_name='contests')
    title = models.CharField(max_length=128)
    start_time = models.DateTimeField(null=True, blank=True)
    length = models.IntegerField(default=300)
    board_stop = models.IntegerField(default=300)
    desc = models.TextField(default='')
    lang_limit = models.IntegerField(default=0)
    contest_type = models.IntegerField(default=0, choices=conf.CONTEST_TYPE.choice())
    printer_url = models.CharField(max_length=64, null=True, default=None)

    def __init__(self, *args, **kwargs):
        super(Contest, self).__init__(*args, **kwargs)
        if self.start_time:
            self._start_time = self.start_time.replace(tzinfo=None)

    def __unicode__(self):
        return self.title

    def key(self):
        return 'contest__' + str(self.pk)

    def change_by_user(self, user):
        return user.has_perm('ojuser.change_groupprofile', self.group)

    @property
    def lang_limited(self):
        res = []
        for x in conf.LANGUAGE_MASK.choice():
            if x[0] & self.lang_limit:
                res.append(x[0])
        return res

    @lang_limited.setter
    def lang_limited(self, value):
        res = 0
        for x in value:
            res |= int(x)
        self.lang_limit = res

    def get_date_time(self):
        return self._start_time.date(), self._start_time.time()

    def server_time(self):
        dtime = datetime.now()
        return time.mktime(dtime.timetuple())

    def time_left(self):
        now = datetime.now()
        if now < self._start_time:
            return self.length
        if now > self._start_time + timedelta(minutes=self.length):
            return 0
        return int((self._start_time + timedelta(minutes=self.length) -now).total_seconds())

    def time_passed_precent(self):
        now = datetime.now()
        if now < self._start_time:
            return 0
        if now > self._start_time + timedelta(minutes=self.length):
            return 100
        return int(((now - self._start_time).total_seconds())*100/(self.length*60))

    def ended(self):
        now = datetime.now()
        if now < self._start_time:
            return -1
        if now > self._start_time + timedelta(minutes=self.length):
            return 1
        return 0

    def last_notification(self):
        if self.notifications.count() == 0:
            return None
        return self.notifications.last().title

    def get_board_seal_time(self):
        return self.start_time + timedelta(minutes=self.board_stop)

    def type_is_icpc(self):
        return self.contest_type == conf.CONTEST_TYPE_ICPC or self.contest_type == conf.CONTEST_TYPE_ICPC_MANUAL

    def type_is_oi(self):
        return self.contest_type == conf.CONTEST_TYPE_OI


class ContestProblem(models.Model):
    contest = models.ForeignKey(Contest, related_name='problems')
    problem = models.ForeignKey(Problem)
    score = models.IntegerField(default=0)
    index = models.CharField(default='A',max_length=2)
    ac_sub = models.IntegerField(default=0)
    all_sub = models.IntegerField(default=0)
    title = models.CharField(max_length=64, default='')

    def __unicode__(self):
        return self.index + '. ' + self.title

class Notification(models.Model):

    contest = models.ForeignKey(Contest, related_name='notifications')
    title = models.CharField(max_length=128)
    content = models.TextField(default='')
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class Clarification(models.Model):

    author = models.ForeignKey(User, related_name='clarifications')
    question = models.TextField(default='')
    answer = models.TextField(default='')
    create_time = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey(Contest, related_name='clarifications')


class ProblemRecord(object):

    def __init__(self, _idx):
        self.AC = 0
        self.sub = 0
        self.pen = 0
        self.ac_time = 0
        self.idx = _idx
        self.first_blood = False

    def to_json(self):
        return {
            'AC': self.AC,
            'sub': self.sub,
            'pen': self.pen,
            'ac_time': self.ac_time,
            'idx': self.idx,
            'fb': self.first_blood
        }


class BoradRecord(object):

    def __init__(self, username, nickname):
        self.problems = {}
        self.username = username
        self.nickname = nickname
        self.AC = 0
        self.sub = 0
        self.pen = 0

    def add_problem(self, idx, problem):
        self.problems[idx] = problem

    #calc user rank
    def calc(self, probs, contest_type):
        for prob in probs:
            if not self.problems.has_key(prob.index):
                self.problems[prob.index] = ProblemRecord(prob.index)
        self.problems = self.problems.values()
        self.problems.sort(key=lambda x: x.idx)
        for sinfo in self.problems:
            if sinfo.AC > 0:
                self.AC += 1
                if contest_type == 0:
                    self.pen += sinfo.pen + sinfo.ac_time
            if contest_type == 1:
                self.pen += sinfo.pen
            self.sub += sinfo.sub

    def to_json(self):
        return {
            'sub': self.sub,
            'AC': self.AC,
            'pen': self.pen,
            'username': self.username,
            'nickname': self.nickname,
            'problems': [x.to_json() for x in self.problems]
        }


class Submission(AbstractSubmission):

    problem = models.ForeignKey(ContestProblem, related_name='contest_submissions')
    user = models.ForeignKey(User, related_name='contest_submissions')

    class Meta:
        db_table = 'contest_submission'

    def get_problem(self):
        return self.problem.problem

    def get_submission_type(self):
        return "contest"

    def add_socre(self, position):
        pass

    def deal_case_result(self, case):
        super(Submission, self).deal_case_result(case)
        if case['status'] == 'AC' and case['position'] == self.get_problem().cases.count() - 1:
            self.problem.ac_sub += 1
            self.problem.save()

        # Calculate score for OI mode
        score = 0
        if case['status'] != 'AC' or case['position'] == self.get_problem().cases.count() - 1:
            case_entities = self.problem.problem.cases.order_by('position').all()
            for case_result in self.cases:
                if case_result['status'] == 'AC':
                    case_index = case_result['position']
                    if 0 <= case_index < case_entities.count():
                        score += case_entities[case_index].score
        self.score = score
        self.save()

    def get_id(self):
        return self.pk

