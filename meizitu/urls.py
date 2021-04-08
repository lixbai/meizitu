from django.urls import path, include
from apps.album import views as album_views
from apps.news import views as news_views
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from apps.album.models import Album, AlbumTags
from apps.beauty.models import Beauty, BeautyTags
from apps.news.models import News


album_info_dict = {
    'queryset': Album.objects.all(),
    'date_field':'modify_time',
    'changefreq':2
}
albumtag_info_dict = {
    'queryset': AlbumTags.objects.all(),
}

sitemaps_dict = {
    'album': GenericSitemap(album_info_dict, priority=0.6),
    'album_tag': GenericSitemap(albumtag_info_dict, priority=0.5),
    'beauty': GenericSitemap({'queryset': Beauty.objects.all(),'date_field':'modify_time'}, priority=0.6),
    'beauty_tag': GenericSitemap({'queryset': BeautyTags.objects.all(),}, priority=0.5),
    'news': GenericSitemap({'queryset': News.objects.all(), 'date_field':'pub_time'}, priority=0.7),
}

urlpatterns = [
    path('', news_views.news_index, name='news_index'), #这里把news的首页当作网站的首页
    path ('search/', news_views.search, name='search'),

    path('news/', include('apps.news.urls')),
    path('album/', include('apps.album.urls')),
    path('beauty/', include('apps.beauty.urls')),

    path('cms/', include('apps.cms.urls')),
    path('account/', include('apps.mzauth.urls')),

    path('ueditor/', include('apps.ueditor.urls')),

    path('__debug__/', include(debug_toolbar.urls)),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps_dict}, name='django.contrib.sitemaps.views.sitemap'),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
