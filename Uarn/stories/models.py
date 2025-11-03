from django.db import models
from django.utils import timezone

class Story(models.Model):
    GENRE_CHOICES = [
        ('love', 'Романтика'),
        ('horror', 'Ужасы'),
        ('fantasy', 'Фантастика'),
        ('life', 'Из жизни'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True, default="Аноним")
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='other')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} ({self.get_genre_display()})"
