from django.db import models

class Movie(models.Model):
    LANGUAGES = [
        ('BO', 'Bollywood'),
        ('MA', 'Marathi'),
        ('EN', 'English')
    ]
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    year = models.IntegerField()
    poster = models.ImageField(upload_to='posters/')

class Clue(models.Model):
    CLUE_TYPES = [
        ('IMG', 'Image'),
        ('DLG', 'Dialogue'),
        ('RDL', 'Riddle')
    ]
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    clue_type = models.CharField(max_length=3, choices=CLUE_TYPES)
    content = models.TextField()  # Text for dialogues/riddles, URL for images
    difficulty = models.IntegerField(default=1)  # 1-3 scale