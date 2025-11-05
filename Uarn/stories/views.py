from django.shortcuts import render, redirect
from .models import Story, Tag
from .forms import StoryForm
from django.http import JsonResponse

def index(request):
    stories = Story.objects.all()
    tags = Tag.objects.all()
    tag_filter = request.GET.get('tag')

    if tag_filter:
        stories = stories.filter(tags__name=tag_filter)

    return render(request, 'stories/index.html', {
        'stories': stories,
        'tags': tags,
        'selected_tag': tag_filter,
    })


from .models import Story, Tag

def add_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.save()

            # Обработка тегов
            tags_input = form.cleaned_data.get('tags_input', '')
            tag_names = [t.strip() for t in tags_input.split(',') if t.strip()]
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                story.tags.add(tag)

            return redirect('stories:index')
    else:
        form = StoryForm()

    # Передаём все существующие теги для автоподсказки
    tags = Tag.objects.all()
    return render(request, 'stories/add_story.html', {'form': form, 'tags': tags})


def search_stories(request):
    query = request.GET.get('q', '')
    stories = Story.objects.filter(title__icontains=query) | Story.objects.filter(content__icontains=query)
    results = list(stories.values('id', 'title', 'author'))
    return JsonResponse({'results': results})
