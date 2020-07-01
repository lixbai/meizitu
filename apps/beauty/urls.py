from django.urls import path
from . import views

app_name='beauty'

urlpatterns = [
    path('', views.index, name='beauty_index'),
    path('detail/<int:beauty_id>/', views.beauty_detail, name='beauty_detail')
]