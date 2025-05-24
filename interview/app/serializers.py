from rest_framework import serializers
from .models import InterviewQuestion,Comment

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


# class CommentSerializer(serializers.ModelSerializer):
#     # 不再使用UserSerializer
#     user_info = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Comment
#         fields = ['id', 'user_id', 'user_info', 'content', 'created_at', 'parent', 'replies']
#
#     def get_user_info(self, obj):
#         # 返回缓存的用户信息或从外部系统获取
#         return {
#             'username': obj.username,
#             'avatar': obj.user_avatar
#         }
#
#     def get_replies(self, obj):
#         if obj.replies.exists():
#             return CommentSerializer(obj.replies.all(), many=True).data
#         return None


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
            'content': {'required': True},
            'user_id': {'required': True}
        }

    def validate(self, data):
        if not data.get('content'):
            raise serializers.ValidationError("评论内容不能为空")
        if not data.get('user_id'):
            raise serializers.ValidationError("用户ID不能为空")
        return data