from django.db import models
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    
class Story(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True, default="Аноним")
    tags = models.ManyToManyField(Tag, related_name='stories', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
