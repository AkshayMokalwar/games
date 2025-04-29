from django.shortcuts import render,redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from movies.models import Clue,Movie
import random
from .models import QuizSession
from users.models import UserProfile
from django.shortcuts import render






def start_quiz(request, session_code):
    # Get 10 random clues based on mode
    # movies = Movie.objects.all()
    clues = Clue.objects.all()
    inverted_dictionary=dict()
    for c in clues:
        # if c.movie.title in ['DDLJ']:
        if c.movie.title not in inverted_dictionary:
            inverted_dictionary[c.movie.title]=[c]
        else:
            inverted_dictionary[c.movie.title].append(c)
    

    print(f"inverted_dictionary : {inverted_dictionary}")
    
    
    
    return render(request, 'quiz/game.html', {
        'clues': clues,
        'session_id': session_code,
        # 'movies': movies,
        'inverted_dictionary':inverted_dictionary
    })

def leaderboard(request):
    time_filter = request.GET.get('filter', 'all-time')
    
    base_query = UserProfile.objects.all().order_by('-total_score')
    
    if time_filter == 'daily':
        # Implement date filtering
        pass
    
    return render(request, 'quiz/leaderboard.html', {
        'users': base_query[:100]
    })