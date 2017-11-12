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



class TestCase(models.Model):

    code_file = models.FileField(null=True, upload_to='code/')
