from django.urls import path
from . import  views

app_name='album'

urlpatterns = [
    path('', views.albums, name='album'),
    path('classic/', views.classic, name='album_classic')
]
