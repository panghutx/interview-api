from rest_framework import serializers
from .models import InterviewQuestion

class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = '__all__'