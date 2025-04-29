from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Authentication routes
    path('quiz/', include('quiz.urls')),  # Game routes
    path('movies/', include('movies.urls')),  # Movie management
    # movie_quiz/urls.py (add this to urlpatterns)
    # path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)