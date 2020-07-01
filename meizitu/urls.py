from django.urls import path, include
from apps.album import views


urlpatterns = [
    path('', views.index, name='album_index'),

    path('news/', include('apps.news.urls')),
    path('album/', include('apps.album.urls')),
    path('beauty/', include('apps.beauty.urls')),

    path('cms/', include('apps.cms.urls')),
    path('account/', include('apps.mzauth.urls'))
]
