from rest_framework import serializers
from .models import Contest, ContestProblem, Clarification, Notification

class ContestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contest

class ContestProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContestProblem

class ClarificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Clarification

class ContestNotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
