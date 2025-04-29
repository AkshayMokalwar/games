from django.urls import path
from . import views

urlpatterns = [
    # API Endpoints (for potential future expansion)
    path('api/movies/', views.movie_list_api, name='movie_list_api'),
    path('api/clues/', views.clue_list_api, name='clue_list_api'),
    
    # Management Views (for admin/staff)
    path('add/', views.add_movie, name='add_movie'),
    path('edit/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('clues/add/<int:movie_id>/', views.add_clue, name='add_clue'),
]