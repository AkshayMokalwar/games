from django.urls import path
from . import views

urlpatterns = [
    # Game Modes
    # path('start/casual/', views.start_quiz, {'mode': 'CS'}, name='start_casual'),
    path('start/casual/<int:session_code>/', views.start_quiz, name='start_casual'),

    path('start/timed/', views.start_quiz, {'mode': 'TM'}, name='start_timed'),
    path('start/daily/', views.start_quiz, {'mode': 'DQ'}, name='start_daily'),

    # # Gameplay
    # path('session/<int:session_id>/', views.quiz_session, name='quiz_session'),
    # path('submit-answer/', views.submit_answer, name='submit_answer'),
    
    # # Lifelines
    # path('hint/<int:clue_id>/', views.get_hint, name='get_hint'),
    # path('skip/<int:clue_id>/', views.skip_clue, name='skip_clue'),
    # path('fifty-fifty/<int:clue_id>/', views.fifty_fifty, name='fifty_fifty'),
    
    # # Results
    # path('results/<int:session_id>/', views.quiz_results, name='quiz_results'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]