from django.urls import path
from . import views

app_name='beauty'

urlpatterns = [
    path('', views.BeautyView.as_view(), name='beauty_index'),

    # path('tags/<int:tag>/', views.tags, name='tags'),
    path('tags/<int:tag>/', views.TagGetBeautyView.as_view(), name='tags'),

    path('detail/<str:uid>/', views.beauty_detail, name='beauty_detail')
]