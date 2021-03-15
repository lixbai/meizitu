from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_index, name='news_index'),# 在根url中映射了，这里就不映射了
    path('detail/<int:news_id>/', views.news_detail, name='news_detail'),
    path('download/', views.download, name='download'),
    path('get_news_by_category/', views.get_news_by_category, name='get_news_by_category'),
    path('list/', views.news_list, name='news_list')
]