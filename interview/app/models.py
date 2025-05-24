from django.db import models

# Create your models here.

from django.db import models
class InterviewQuestion(models.Model):
    DIFFICULTY_LEVELS = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )

    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.CharField(max_length=255, blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100,default='匿名用户')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='Medium')
    category = models.CharField(max_length=100, blank=True, null=True,default='未分类')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'questions'
        managed = False
    def __str__(self):
        return self.title


class Comment(models.Model):
    interview = models.ForeignKey('InterviewQuestion', on_delete=models.CASCADE, related_name='comments')
    user_id = models.CharField(max_length=128)  # 存储用户ID字符串
    username = models.CharField(max_length=150, blank=True)  # 可选：缓存用户名
    user_avatar = models.URLField(blank=True)  # 可选：缓存用户头像URL
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id']),  # 为用户ID添加索引
        ]

    def __str__(self):
        return f'Comment by {self.user.username} on {self.interview.title}'


