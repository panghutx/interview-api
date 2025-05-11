from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
# views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, renderer_classes, api_view
from .models import InterviewQuestion
from rest_framework.renderers import JSONRenderer
from .serializers import InterviewQuestionSerializer

class InterviewQuestionViewSet(viewsets.ModelViewSet):
    queryset = InterviewQuestion.objects.filter(is_active=True)
    serializer_class = InterviewQuestionSerializer

    @api_view(['GET'])
    @renderer_classes([JSONRenderer])
    def get_all_questions(request):
        """获取所有试题"""
        print("请求方法:", request.method)  # 应该是 GET
        if request.method == 'OPTIONS':
            print("这是 OPTIONS 预检请求")
            return Response(status=200)
        elif request.method == 'GET':
            print("这是真正的 GET 请求")
            questions = InterviewQuestion.objects.filter(is_active=True)
            serializer = InterviewQuestionSerializer(questions, many=True)
            return Response(serializer.data)

    @api_view(['POST'])
    def create_question(request):
        """新增试题"""
        serializer = InterviewQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
