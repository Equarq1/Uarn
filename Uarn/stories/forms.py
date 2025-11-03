from django import forms
from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'content', 'author', 'genre']
        labels = {
            'title': 'Заголовок',
            'content': 'Текст истории',
            'author': 'Автор (необязательно)',
            'genre': 'Жанр',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }
