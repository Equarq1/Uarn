from django import forms
from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'content', 'author']
        labels = {
            'title': 'Заголовок',
            'content': 'Текст истории',
            'author': 'Автор (необязательно)',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }
