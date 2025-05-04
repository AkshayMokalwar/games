from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.LoginViews),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('join_room/', views.join_room),
    path('create_room/', views.create_room),
    path('submit_guess/', views.submit_guess),
    path('test_ws/<int:session_code>', views.test_ws),

    # Profile
    path('profile/', views.profile, name='profile'),
    # path('profile/update/', views.update_profile, name='update_profile'),
]