from django.urls import path, include
from apps.album import views as album_views
from apps.news import views as news_views
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('', news_views.news_index, name='news_index'), #这里把news的首页当作网站的首页
    path ('search/', news_views.search, name='search'),
    path('download/', news_views.download, name='download'),

    path('news/', include('apps.news.urls')),
    path('album/', include('apps.album.urls')),
    path('beauty/', include('apps.beauty.urls')),

    path('cms/', include('apps.cms.urls')),
    path('account/', include('apps.mzauth.urls')),

    path('ueditor/', include('apps.ueditor.urls')),

    path('__debug__/', include(debug_toolbar.urls)),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
