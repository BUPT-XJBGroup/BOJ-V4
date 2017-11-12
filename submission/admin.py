from django.contrib import admin
# from .models import Submission
from .abstract_models import NormalSubmission


admin.site.register(NormalSubmission)
