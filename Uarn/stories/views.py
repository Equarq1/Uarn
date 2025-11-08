from django.shortcuts import render, redirect
from .models import Story, Tag
from .forms import StoryForm
from django.http import JsonResponse, Http404
from django.db.models import Q
from .models import Story
import json
import re

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

            # Получаем поле Tagify (оно приходит в JSON)
            tags_data = request.POST.get('tags_input', '[]')
            try:
                tags_list = [t['value'] for t in json.loads(tags_data)]
            except (json.JSONDecodeError, KeyError, TypeError):
                tags_list = []

            # Добавляем теги
            for tag_name in tags_list:
                tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                story.tags.add(tag)

            return redirect('stories:index')
    else:
        form = StoryForm()

    tags = Tag.objects.all()
    return render(request, 'stories/add_story.html', {'form': form, 'tags': tags})


def search_stories(request):
    """
    AJAX поиск.
    Принимает:
      - q     : свободный текст (по title/content/author)
      - tags  : строка с тегами через запятую (tag1,tag2,...)
    Логика:
      - теги применяются как пересечение (AND)
      - текст применяется как OR внутри полей
    Возвращает JSON с полями: id, title, author, excerpt, tags (list)
    """
    q_text = request.GET.get('q', '') or ''
    q_text = q_text.strip()
    tags_param = request.GET.get('tags', '') or ''
    tags_param = tags_param.strip()

    stories_qs = Story.objects.all().order_by('-created_at')

    # обработка тегов (если есть)
    tag_names = []
    # Если явно переданы теги в параметре tags (например tags=tag1,tag2)
    if tags_param:
        # можно принимать как "tag1,tag2" или "#tag1 #tag2" — чистим
        clean = tags_param.replace('#', ' ').replace(',', ' ')
        tag_names = [t.strip() for t in clean.split() if t.strip()]
    else:
        # Попробуем извлечь теги из текстового поля q (токены, начинающиеся с '#')
        # Пример: q="#tag1 #tag2 some text" или q="#тег1 текст"
        if q_text:
            found = re.findall(r"#([^\s#]+)", q_text)
            if found:
                tag_names = [t.strip() for t in found if t.strip()]
                # Удалим найденные теги из текстового запроса, чтобы не мешали поиску по тексту
                q_text = re.sub(r"#([^\s#]+)", ' ', q_text).strip()

    # Применяем фильтр по тегам (пересечение)
    for tag_name in tag_names:
        stories_qs = stories_qs.filter(tags__name__iexact=tag_name)

    # обработка текста (если есть)
    if q_text:
        parts = [p.strip() for p in q_text.split() if p.strip()]
        if parts:
            qobj = Q()
            for p in parts:
                qobj |= Q(title__icontains=p) | Q(content__icontains=p) | Q(author__icontains=p)
            stories_qs = stories_qs.filter(qobj)

    stories_qs = stories_qs.distinct()[:100]

    results = []
    for s in stories_qs:
        results.append({
            'id': s.id,
            'title': s.title,
            'author': s.author or 'Аноним',
            'excerpt': (s.content[:300] + '...') if len(s.content) > 300 else s.content,
            'tags': [t.name for t in s.tags.all()],
        })
    return JsonResponse({'results': results})


def story_detail(request, story_id):
    """Отображает страницу с полным текстом истории"""
    try:
        story = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        raise Http404("История не найдена")
    
    return render(request, 'stories/story_detail.html', {'story': story})

def story_detail_ajax(request, story_id):
    """Возвращает полный текст истории для AJAX-запроса"""
    try:
        s = Story.objects.get(pk=story_id)
    except Story.DoesNotExist:
        raise Http404("История не найдена")

    return JsonResponse({
        'id': s.id,
        'title': s.title,
        'author': s.author or 'Аноним',
        'content': s.content,
        'tags': [t.name for t in s.tags.all()],
    })
