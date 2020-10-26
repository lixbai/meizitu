from django.db import models
from apps.beauty.models import Beauty
from shortuuidfield import ShortUUIDField
import os

#图集标签类
class AlbumTags(models.Model):
    tag = models.CharField(max_length=40, verbose_name='图集标签', error_messages={'max_length':'最长为40位', 'min_length':'最短是0位'})


#创建存放图集封面图片的文件夹函数
#类似文件路径: /media/album/uid/xx.jpg
def create_album_folder(instance, filename):
    return os.path.join('album/', instance.uid, filename)

#图集类
class Album(models.Model):
    '''
    图集项目
    浏览次数	封面img	标题	图集tags	图集介绍 姓名	创建时间	修改时间	下载链接	下载密码	价格
                        图集tags
                        图集tags
                        多对多
    '''
    #用
    uid = ShortUUIDField(primary_key=True)
    watch_count = models.IntegerField(verbose_name='浏览次数', default=9000)
    title = models.CharField(max_length=300, verbose_name='标题')
    desc = models.TextField(verbose_name='图集介绍')
    beauty_name = models.CharField(max_length=30, verbose_name='女神姓名')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    download_url = models.TextField(verbose_name='下载链接')
    download_password = models.CharField(max_length=30, verbose_name='下载密码')
    download_price = models.FloatField(verbose_name='图集价格')

    cover_img = models.ImageField(upload_to=create_album_folder)
    #和图集标签多对多的关系
    tags = models.ManyToManyField(to=AlbumTags, related_name='album_tags')

    #和Beauty多对一, 图集多,美女一
    beauty = models.ForeignKey(to=Beauty, on_delete=models.CASCADE, related_name='album')

    class Meta:
        ordering = ['-create_time']


#定义存放图片的路径位置:
#路径如:/media/pic/uuid/xx.jpg
#这里会用到外键的uid
def create_pic_folder(instance, filename):
    #注意在这个函数中用到的instance.album.uid是album的主键,是用到的外键,这样/pic/uid/xx.jpg中的uid就是album中的uid了.
    return os.path.join('pic/', instance.album.uid, filename)


#图片类
class Pic(models.Model):
    '''
    图片表
    图片url1
    图片url2
    图片url3
    外键
    '''
    picture = models.ImageField(upload_to=create_pic_folder)

    #需要用到指向Album的外键,图片和图集类是多对一的关系
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE, related_name='pic')