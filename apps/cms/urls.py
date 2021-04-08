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

    #处理图集
    path('write_album/', views.WriteAlbumView.as_view(), name='write_album'),

    #处理图集图片
    path('write_pic/', views.PicView.as_view(), name='write_pic'),

    #处理美女的标签
    path('write_beauty_tag/', views.WriteBeautyTagView.as_view(), name='write_beauty_tag'),
    path('edit_beauty_tag/', views.edit_beauty_tag, name='edit_beauty_tag'),
    path('delete_beauty_tag/', views.delete_beauty_tag, name='delete_beauty_tag'),

    #处理美女
    path('write_beauty/', views.WriteBeautyView.as_view(), name='write_beauty'),

    # 处理消息的分类
    path('write_news_category/', views.WriteNewsCategory.as_view(), name='write_news_category'),
    path('edit_news_category/', views.edit_news_category, name='edit_news_category'),
    path('del_news_category/', views.del_news_category, name='del_news_category'),

    # 处理文章的tag
    path('news_add_tags/', views.news_add_tags, name='news_add_tags'),
    path('news_edit_tags/', views.news_edit_tags, name='news_edit_tags'),
    path('news_del_tags/', views.news_del_tags, name='news_del_tags'),

    # 处理消息news
    path('write_news/', views.WriteNews.as_view(), name='write_news'),
    path('ajax_news_post/', views.ajax_news_post, name='ajax_news_post'),


    #news上传图片用到的.
    path('upload_files/', views.upload_files, name='upload_files'),
    # path('upload_cloud_files/', views.aliyun_oss_tencent_cos_local_upload_files, name='upload_cloud_files'),

]