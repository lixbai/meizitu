from django.urls import path, include

urlpatterns = [
    path('', include('apps.news.urls')),
    path('cms/', include('apps.cms.urls')),
    path('account/', include('apps.mzauth.urls'))
]
