from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InterviewQuestionViewSet,CommentListCreateView

router = DefaultRouter()
router.register(r'interview-questions', InterviewQuestionViewSet)

urlpatterns = [
    path('interview-questions/', InterviewQuestionViewSet.get_all_questions, name='get_all_questions'),
    path('interview-questions/new/', InterviewQuestionViewSet.create_question, name='create_question'),
    path('interview-questions/<int:pk>/', InterviewQuestionViewSet.get_question, name='get_question'),
    path('interview-questions/<int:pk>/edit/', InterviewQuestionViewSet.update_question, name='update_question'),
    path('interview-questions/<int:pk>/delete/', InterviewQuestionViewSet.delete_question, name='delete_question'),
    path('interviews/<int:interview_id>/comments/',
         CommentListCreateView.get_comments,
         name='comment-list'),
    path('interviews/<int:interview_id>/comments/create/',
         CommentListCreateView.create_comment,
         name='comment-create'),
]
