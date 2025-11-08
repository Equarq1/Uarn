from django.urls import path
from . import views

app_name = 'stories'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_story, name='add_story'),
    path('search/', views.search_stories, name='search_stories'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
    path('story/<int:story_id>/ajax/', views.story_detail_ajax, name='story_detail_ajax'),

]
