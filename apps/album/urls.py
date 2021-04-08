from django.urls import path, re_path
from . import  views
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from .models import Album

info_dict = {
    'queryset': Album.objects.all(),
    'date_field': 'create_time',
}

app_name='album'

urlpatterns = [
    path('', views.AlbumsView.as_view(), name='album'),

    path('tags/<path:tag>', views.TagGetAlbumView.as_view(), name='tags'),
    # path('show_pic/<str:uid>/', views.ShowPicView.as_view(), name='show_pic'),
    path('show_pic/<str:uid>/<path:title>', views.ShowPicView.as_view(), name='show_pic'),


    path('sitemap.xml', sitemap, {'sitemaps':{'album': GenericSitemap(info_dict, priority=0.6)}}, name='django.contrib.sitemaps.views.sitemap')
]
