import os, sys
import django
from django.core.files.base import ContentFile
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'bojv4.settings'
django.setup()

from filer.models.filemodels import File
from submission.models import Submission as OldSubmission
from submission.abstract_models import NormalSubmission
from contest.models import Submission as ContestSubmission
from contest.models import ContestSubmission as OldContestSubmission


if __name__ == '__main__':
    cs_ids = set()

    cs = OldContestSubmission.objects.all()
    for o in cs:
        cs_ids.add(o.submission_id)
        s = ContestSubmission()
        oc = o.submission
        s.user = oc.user
        s.problem = o.problem
        s.code_file = oc.code_file
        s.status = oc.status
        s.create_time = oc.create_time
        s.score = oc.score
        s.language = oc.language
        s.info = oc.info
        for c in oc.cases.all():
            case = {}
            case['position'] = c.position
            case['time'] = c.running_time
            case['memory'] = c.running_memory
            case['status'] = c.status
            s.add_case(case)
        s.save()

    '''
    ss = OldSubmission.objects.all()
    for o in ss:
        if o.pk in cs_ids:
            continue
        s = NormalSubmission()
        s.user = o.user
        s.problem = o.problem
        s.code_file = o.code_file
        s.status = o.status
        s.create_time = o.create_time
        s.score = o.score
        s.language = o.language
        s.info = o.info
        for c in o.cases.all():
            case = {}
            case['position'] = c.position
            case['time'] = c.running_time
            case['memory'] = c.running_memory
            case['status'] = c.status
            s.add_case(case)
        s.save()
    '''



