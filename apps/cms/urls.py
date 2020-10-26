from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    #进入后台首页
    path('', views.index, name='cms_index'),

    #处理图集标签的视图
    path('write_album_tag/', views.WriteAblumTagView.as_view(), name='write_album_tag'),
    path('edit_album_tags/', views.edit_album_tags, name='edit_album_tags'),
    path('del_album_tags/', views.del_album_tags, name='del_album_tags'),

    #处理美女的标签
    path('write_beauty_tag/', views.WriteBeautyTagView.as_view(), name='write_beauty_tag'),
    path('edit_beauty_tag/', views.edit_beauty_tag, name='edit_beauty_tag'),
    path('delete_beauty_tag/', views.delete_beauty_tag, name='delete_beauty_tag'),

    #处理美女
    path('write_beauty/', views.WriteBeautyView.as_view(), name='write_beauty'),

    #news上传图片用到的.
    path('upload_files/', views.upload_files, name='upload_files')
]