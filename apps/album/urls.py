from django.urls import path
from . import  views

app_name='album'

urlpatterns = [
    path('', views.albums, name='album'),
    path('<int:album_id>', views.album_detail, name='album_detail')
]
