from rest_framework import serializers
from .abstract_models import NormalSubmission as Submission
from problem.models import Problem


class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Submission

