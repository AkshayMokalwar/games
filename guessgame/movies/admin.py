from django.contrib import admin
from .models import Movie, Clue

class ClueInline(admin.TabularInline):
    model = Clue
    extra = 3

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [ClueInline]
    list_filter = ['language', 'year']
    search_fields = ['title']