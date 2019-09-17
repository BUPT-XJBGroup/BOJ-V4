from __future__ import unicode_literals
import json

from django.contrib.auth.models import User
from filer.models.filemodels import File
from filer.fields.file import FilerFileField
from django.core.urlresolvers import reverse
from django.db import models
from ojuser.models import GroupProfile
from django.core.cache import cache
from bojv4.settings import BASE_DIR
from django.core.cache import cache

#  from filer.fields.file import FilerFileField


class ProblemTag(models.Model):
    name = models.CharField(max_length=50)


class Problem(models.Model):

    FORBIDDEN_TIMEOUT = 24 * 3600 * 60
    HITS_LIMIT = 30
    SUBMIT_INTERVAL = 300
    

    title = models.CharField(max_length=50, default='Untitled')
    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=65536)
    code_length_limit = models.IntegerField(default=65536)
    desc = models.TextField(default='None')
    is_checked = models.BooleanField(default=False)
    superadmin = models.ForeignKey(User)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    # allowed_lang = models.ManyToManyField('ojuser.Language', related_name='problems')
    groups = models.ManyToManyField(GroupProfile, blank=True, related_name='problems')
    tags = models.ManyToManyField(ProblemTag, blank=True, related_name='problems')
    is_spj = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('problem:problem-detail', kwargs={'pk': self.pk})

    def view_by_user(self, user):
        for g in self.groups.all():
            if user.has_perm('ojuser.view_groupprofile', g):
                return True
        return False

    @classmethod
    def is_forbid(cls, user):
        forbid_key = 'forbid_submit_' + user.username
        if cache.get(forbid_key):
            return True
        return False
        
    def forbid(self, user):
        cache_key = str(self.pk) + "_forbid_" + user.username
        hits = cache.get(cache_key)
        if not hits:
            cache.set(cache_key, 1, self.SUBMIT_INTERVAL)
            return False
        forbid_key = 'forbid_submit_' + user.username
        if cache.get(forbid_key):
            return True
        cache.incr(cache_key, 1)
        if hits > self.HITS_LIMIT:
            cache.set(forbid_key, 1, self.FORBIDDEN_TIMEOUT)
            return True
        return False
        
    def description(self):
        if not hasattr(self, '_desc'):
            try:
                self._desc = json.loads(self.desc)
            except:
                self._desc = {'desc': self.desc, 'sample_in': '', 'sample_out': ''}
        return self._desc['desc']

    def sample_in(self):
        if not hasattr(self, '_desc'):
            try:
                self._desc = json.loads(self.desc)
            except:
                self._desc = {'desc': self.desc, 'sample_in': '', 'sample_out': ''}
        return self._desc['sample_in']

    def sample_out(self):
        if not hasattr(self, '_desc'):
            try:
                self._desc = json.loads(self.desc)
            except:
                self._desc = {'desc': self.desc, 'sample_in': '', 'sample_out': ''}
        return self._desc['sample_out']

    def check_data(self):
        data_info = self.datainfo
        in_set = set()
        out_set = set()
        mp = {}
        self.cases.all().delete()
        for f in data_info.all():
            data = f.data
            path = data.path
            filename = path[path.rfind('/') + 1:]
            mp[filename] = data
            if path.endswith('.in'):
                if filename in in_set:
                    return False
                in_set.add(filename)
            elif path.endswith('.out'):
                if filename in out_set:
                    return False
                out_set.add(filename)
        if len(in_set) !=  len(out_set):
            return False
        cases = []
        for x in in_set:
            case = ProblemCase()
            case.problem = self
            case.input_data = mp[x]
            case.position = len(cases)
            outfile = x.rstrip('.in') + '.out'
            if outfile in out_set:
                case.output_data = mp[outfile]
            else:
                return False
            case.gen_sample_data()
            cases.append(case)
        for cas in cases:
            cas.save()
        return True

    def get_problem_data(self):
        resp = []
        p_count = 0
        for cas in self.cases.all():
            in_data = cas.input_data.path
            out_data = cas.output_data.path
            resp.append({
                'in': in_data,
                'out': out_data,
                'position': p_count
                })
            p_count += 1
        return resp

    def get_position_data(self, position):
        if not self.cases or self.cases.count() <= position:
            return None, None
        case = self.cases.all()[position]
        return case.sample_in, case.sample_out

    def get_score(self, position):
        if not isinstance(position, int) or position >= self.cases.count():
            raise Exception("param 'position' is invalid.")
        return self.cases.all()[position].score

    @property
    def score(self):
        res = 0
        for c in self.cases.all():
            res += c.score
        return res

    class Meta:
        permissions = (
            ('view_problem', 'Can view problem'),
        )


def upload_dir(instance, filename):
    return 'documents/{0}/{1}'.format(instance.problem.pk, str(filename))


class ProblemDataInfo(models.Model):
    problem = models.ForeignKey(Problem, related_name="datainfo")
    data = models.OneToOneField(File, null=True, blank=True, related_name="datainfo")

    def __unicode__(self):
        return str(self.problem.pk) + " " + str(self.pk)


class ProblemCase(models.Model):
    problem = models.ForeignKey(Problem, related_name="cases")
    input_data = models.OneToOneField(File, null=True, blank=True, related_name="incase")
    output_data = models.OneToOneField(File, null=True, blank=True, related_name="outcase")
    sample_in = models.CharField(max_length=256, blank=True, null=True)
    sample_out = models.CharField(max_length=256, blank=True, null=True)
    score = models.IntegerField(default=0)
    position = models.IntegerField(default=0)
    info = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.problem.pk) + ":" + str(self.pk)

    @property
    def input_name(self):
        path = self.input_data.path
        return path[path.rfind('/') + 1:]

    @property
    def output_name(self):
        path = self.output_data.path
        return path[path.rfind('/') + 1:]

    @staticmethod
    def get_data_from_file(path, limit=200):
        data = ''
        with open(path, 'r') as f:
            data = f.read(limit)
        return data

    def gen_sample_data(self):
        self.sample_in = self.get_data_from_file(self.input_data.path, 200)
        self.sample_out = self.get_data_from_file(self.output_data.path, 200)



