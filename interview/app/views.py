from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# views.py

from rest_framework import viewsets, status,generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action, renderer_classes, api_view
from .models import InterviewQuestion,Comment
from rest_framework.renderers import JSONRenderer
from .serializers import InterviewQuestionSerializer,CommentSerializer

class InterviewQuestionViewSet(viewsets.ModelViewSet):
    queryset = InterviewQuestion.objects.filter(is_active=True)
    serializer_class = InterviewQuestionSerializer

    # @api_view(['GET'])
    # @renderer_classes([JSONRenderer])
    # def get_all_questions(request):
    #     """获取所有试题"""
    #     print("请求方法:", request.method)  # 应该是 GET
    #     if request.method == 'OPTIONS':
    #         print("这是 OPTIONS 预检请求")
    #         return Response(status=200)
    #     elif request.method == 'GET':
    #         print("这是真正的 GET 请求")
    #         questions = InterviewQuestion.objects.filter(is_active=True)
    #         serializer = InterviewQuestionSerializer(questions, many=True)
    #         return Response(serializer.data)

    @api_view(['GET'])
    @renderer_classes([JSONRenderer])
    def get_all_questions(request):
        questions = InterviewQuestion.objects.filter(is_active=True).order_by('-id')

        paginator = PageNumberPagination()
        paginator.page_size = 6  # 每页6条

        page = paginator.paginate_queryset(questions, request)
        if page is not None:
            serializer = InterviewQuestionSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = InterviewQuestionSerializer(questions, many=True)
        return Response(serializer.data)

    @api_view(['POST'])
    def create_question(request):
        """新增试题"""
        print("Request Data:", request.data)
        serializer = InterviewQuestionSerializer(data=request.data)
        print(request)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @renderer_classes([JSONRenderer])
    def get_question(request, pk):
        """获取指定 ID 的试题"""
        try:
            question = InterviewQuestion.objects.get(pk=pk, is_active=True)
        except InterviewQuestion.DoesNotExist:
            return Response({"error": "试题不存在"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InterviewQuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(['PUT'])
    def update_question(request, pk):
        """更新指定 ID 的试题"""
        try:
            question = InterviewQuestion.objects.get(pk=pk, is_active=True)
        except InterviewQuestion.DoesNotExist:
            return Response({"error": "试题不存在"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InterviewQuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['DELETE'])
    def delete_question(request, pk):
        """删除指定 ID 的试题"""
        try:
            question = InterviewQuestion.objects.get(pk=pk, is_active=True)
        except InterviewQuestion.DoesNotExist:
            return Response({"error": "试题不存在"}, status=status.HTTP_404_NOT_FOUND)

        question.is_active = False
        question.save()
        return Response({"message": "删除成功"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """自定义接口：增加浏览次数"""
        question = self.get_object()
        question.views += 1
        question.save()
        return Response({'views': question.views}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def increment_likes(self, request, pk=None):
        """自定义接口：增加点赞次数"""
        question = self.get_object()
        question.likes += 1
        question.save()
        return Response({'likes': question.likes}, status=status.HTTP_200_OK)


class CommentListCreateView(viewsets.ModelViewSet):
    """
    组合视图：同时支持查看和创建评论
    GET - 无需认证
    POST - 需要认证
    """
    serializer_class = CommentSerializer
    permission_classes = []

    @api_view(['GET'])
    @renderer_classes([JSONRenderer])
    def get_comments(request, interview_id):
        """获取指定面试题的所有评论"""
        try:
            # 先验证面试题是否存在
            InterviewQuestion.objects.get(pk=interview_id, is_active=True)

            # 获取该面试题的所有顶级评论(非回复)
            comments = Comment.objects.filter(
                interview_id=interview_id,
                parent__isnull=True
            ).order_by('-created_at')

        except InterviewQuestion.DoesNotExist:
            return Response({"error": "面试题不存在"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @api_view(['POST'])
    @renderer_classes([JSONRenderer])
    def create_comment(request, interview_id):
        """为指定面试题创建评论"""
        try:
            print("请求数据:", request.data)  # 调试输出

            # 验证面试题是否存在
            InterviewQuestion.objects.get(pk=interview_id, is_active=True)

            # 准备评论数据
            comment_data = {
                'interview': interview_id,
                'content': request.data.get('content'),
                'user_id': request.data.get('user_id'),
                'username': request.data.get('username', ''),
                'user_avatar': request.data.get('user_avatar', ''),
                'parent': request.data.get('parent')
            }
            print("准备的数据:", comment_data)  # 调试输出

            serializer = CommentSerializer(data=comment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            print("序列化错误:", serializer.errors)  # 调试输出
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except InterviewQuestion.DoesNotExist:
            return Response({"error": "面试题不存在"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("服务器错误:", str(e))  # 调试输出
            return Response({"error": "服务器错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)