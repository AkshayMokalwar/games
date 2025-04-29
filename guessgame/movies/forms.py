from django import forms
from .models import Movie, Clue

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'language', 'year', 'poster']
        widgets = {
            'year': forms.NumberInput(attrs={'min': 1900, 'max': 2100}),
            'language': forms.Select(choices=Movie.LANGUAGES)
        }

class ClueForm(forms.ModelForm):
    class Meta:
        model = Clue
        fields = ['movie', 'clue_type', 'content', 'difficulty']
        widgets = {
            'clue_type': forms.Select(choices=Clue.CLUE_TYPES),
            'difficulty': forms.NumberInput(attrs={'min': 1, 'max': 3}),
            'content': forms.Textarea(attrs={'rows': 3})
        }

class ClueFilterForm(forms.Form):
    LANGUAGE_CHOICES = [('', 'All')] + Movie.LANGUAGES
    DIFFICULTY_CHOICES = [
        ('', 'Any'),
        (1, 'Easy'),
        (2, 'Medium'),
        (3, 'Hard')
    ]

    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, required=False)
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, required=False)
    clue_type = forms.ChoiceField(choices=[('', 'All')] + Clue.CLUE_TYPES, required=False)