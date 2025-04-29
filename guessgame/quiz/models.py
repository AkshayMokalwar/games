from django.db import models
from users.models import UserProfile
from movies.models import Clue

class QuizSession(models.Model):
    session_code = models.CharField(max_length=8, unique=True)
    host = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='hosted_quiz_sessions'  # unique name
    )
    participants = models.ManyToManyField(
        UserProfile,
        related_name='joined_quiz_sessions'  # another unique name
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    mode = models.CharField(max_length=2, choices=[
        ('CS', 'Casual'),
        ('TM', 'Timed'),
        ('DQ', 'Daily')
    ])
    score = models.IntegerField(default=0)
    current_question_index = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def get_participants(self, obj):
        return ", ".join([p.user.username for p in obj.participants.all()])
    get_participants.short_description = 'Participants'


class UserAnswer(models.Model):
    session = models.ForeignKey(QuizSession, on_delete=models.CASCADE)
    clue = models.ForeignKey(Clue, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    lifelines_used = models.JSONField(default=dict)