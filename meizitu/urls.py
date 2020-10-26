from django.urls import path, include
from apps.album import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='login'),

    path('news/', include('apps.news.urls')),
    path('album/', include('apps.album.urls')),
    path('beauty/', include('apps.beauty.urls')),

    path('cms/', include('apps.cms.urls')),
    path('account/', include('apps.mzauth.urls')),

    path('ueditor/', include('apps.ueditor.urls'))
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
