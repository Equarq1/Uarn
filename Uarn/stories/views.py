from django.shortcuts import render, redirect
from .models import Story
from .forms import StoryForm

def index(request):
    genre_filter = request.GET.get('genre')
    stories = Story.objects.all()
    genres = Story.objects.values_list('genre', flat=True).distinct()

    if genre_filter:
        stories = stories.filter(genre=genre_filter)

    return render(request, 'stories/index.html', {
        'stories': stories,
        'genres': genres,
        'selected_genre': genre_filter,
    })


def add_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = StoryForm()
    return render(request, 'stories/add_story.html', {'form': form})