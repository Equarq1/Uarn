from django.urls import path
from . import views

app_name = 'stories'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_story, name='add_story'),
]
