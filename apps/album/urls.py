from django.urls import path
from . import  views

app_name='album'

urlpatterns = [
    path('', views.AlbumsView.as_view(), name='album'),

    # path('tags/<int:tag>/', views.tags, name='tags'),
    path('tags/<int:tag>/', views.TagGetAlbumView.as_view(), name='tags'),
    path('show_pic/<str:uid>/', views.show_pic, name='show_pic'),

]
