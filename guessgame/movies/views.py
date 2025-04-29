from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from .models import Movie, Clue
from .forms import MovieForm, ClueForm, ClueFilterForm

# Helper function to check if user is staff
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

# API Views
@require_http_methods(["GET"])
def movie_list_api(request):
    """API endpoint to list all movies"""
    movies = list(Movie.objects.values('id', 'title', 'language', 'year'))
    return JsonResponse({'movies': movies})

@require_http_methods(["GET"])
def clue_list_api(request):
    """API endpoint to list all clues with optional filtering"""
    form = ClueFilterForm(request.GET)
    clues = Clue.objects.all()
    
    if form.is_valid():
        if form.cleaned_data['language']:
            clues = clues.filter(movie__language=form.cleaned_data['language'])
        if form.cleaned_data['difficulty']:
            clues = clues.filter(difficulty=form.cleaned_data['difficulty'])
        if form.cleaned_data['clue_type']:
            clues = clues.filter(clue_type=form.cleaned_data['clue_type'])
    
    clue_data = list(clues.values(
        'id', 
        'movie__title', 
        'clue_type', 
        'content', 
        'difficulty'
    ))
    return JsonResponse({'clues': clue_data})

# Management Views
@staff_required
@login_required
def add_movie(request):
    """View for adding new movies to the database"""
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            return redirect('add_clue', movie_id=movie.id)
    else:
        form = MovieForm()
    
    return render(request, 'movies/add_movie.html', {
        'form': form,
        'title': 'Add New Movie'
    })

@staff_required
@login_required
def edit_movie(request, movie_id):
    """View for editing existing movies"""
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)
    
    return render(request, 'movies/add_movie.html', {
        'form': form,
        'title': f'Edit {movie.title}',
        'movie': movie
    })

@staff_required
@login_required
def add_clue(request, movie_id):
    """View for adding clues to a specific movie"""
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if request.method == 'POST':
        form = ClueForm(request.POST)
        if form.is_valid():
            clue = form.save(commit=False)
            clue.movie = movie
            clue.save()
            return redirect('add_clue', movie_id=movie.id)
    else:
        form = ClueForm(initial={'movie': movie})
    
    # Get existing clues for this movie
    existing_clues = movie.clue_set.all()
    
    return render(request, 'movies/add_clue.html', {
        'form': form,
        'movie': movie,
        'existing_clues': existing_clues,
        'clue_types': dict(Clue.CLUE_TYPES)
    })

# Additional helpful view (not in URLs but useful)
@login_required
def movie_detail(request, movie_id):
    """View to show movie details and all associated clues"""
    movie = get_object_or_404(Movie, pk=movie_id)
    clues = movie.clue_set.all()
    
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'clues': clues
    })