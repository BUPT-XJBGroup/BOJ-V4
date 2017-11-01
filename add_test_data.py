import os, sys
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'bojv4.settings'
django.setup()

from submission.models import Submission, CaseResult
from contest.models import ContestSubmission, ContestProblem, Contest
from django.contrib.auth.models import User
contest = Contest.objects.first()
group = contest.group
cprob = ContestProblem.objects.first()
problem = cprob.problem
print contest.title
print group.nickname
print problem.title

if __name__ == '__main__':
    with open('./data.count', 'r') as f:
        j = 0
        for x in f.readlines():
            filename = x.split(' ')[0].split(':')[0][2:]
            filename = './cheatdata/' + filename
            s = ContestSubmission()
            u = User(username='testuser__' + str(j), password='123456', email='cheatuser_'+str(j) +'@qq.com')
            j += 1
            u.save()
            group.user_group.user_set.add(u)
            group.save()
            with open(filename, 'r') as f2:
                data = f2.read()
                sub = Submission(problem=problem, user=u, code=data, language='CPP03', status='AC')
                sub.save()
                s.submission = sub
                s.problem = cprob
                s.save()

