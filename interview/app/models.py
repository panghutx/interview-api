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
    author = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='Medium')
    category = models.CharField(max_length=100, blank=True, null=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'questions'
        managed = False
    def __str__(self):
        return self.title

