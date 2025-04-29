from django.contrib import admin

# Register your models here.
from .models import QuizSession,UserAnswer

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ['session_code', 'host', 'mode', 'start_time']
    list_filter = ('mode','host')
    filter_horizontal = ['participants']  # This enables a nice GUI widget

    search_fields = ('user__username',)

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'clue', 'user_answer', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('session__user__username', 'clue__content')