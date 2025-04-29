from django import forms
from movies.models import Movie

class AnswerForm(forms.Form):
    answer = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'placeholder': 'Enter movie name...'
        })
    )
    clue_id = forms.IntegerField(widget=forms.HiddenInput())
    session_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean_answer(self):
        answer = self.cleaned_data['answer'].strip().lower()
        return answer

class QuizSettingsForm(forms.Form):
    MODE_CHOICES = [
        ('CS', 'Casual Mode'),
        ('TM', 'Timed Challenge'),
        ('DQ', 'Daily Quiz')
    ]
    LANGUAGE_CHOICES = [('ALL', 'All Languages')] + Movie.LANGUAGES

    mode = forms.ChoiceField(choices=MODE_CHOICES)
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)
    clue_types = forms.MultipleChoiceField(
        choices=Clue.CLUE_TYPES,
        widget=forms.CheckboxSelectMultiple,
        initial=[ctype[0] for ctype in Clue.CLUE_TYPES]
    )