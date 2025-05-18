from rest_framework import serializers
from .models import InterviewQuestion

class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = '__all__'

    def validate(self, data):
        if not data.get('author'):
            data['author'] = '匿名用户'
        if not data.get('category'):
            data['category'] = '未分类'
        return data