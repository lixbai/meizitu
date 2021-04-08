from django.db import models
from apps.beauty.models import Beauty
from shortuuidfield import ShortUUIDField
import os
# from django.template.defaultfilters import slugify
from uuslug import slugify


#图集标签类
class AlbumTags(models.Model):
    tag = models.CharField(max_length=40, verbose_name='图集标签', error_messages={'max_length':'最长为40位', 'min_length':'最短是0位'})

    def get_absolute_url(self):
        return '/album/tags/%s'%(self.tag)



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
    desc = models.TextField(verbose_name='图集介绍', null=True)
    beauty_name = models.CharField(max_length=30, verbose_name='女神姓名', null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    download_url = models.TextField(verbose_name='下载链接', null=True)
    download_password = models.CharField(max_length=30, verbose_name='下载密码', null=True)
    download_price = models.FloatField(verbose_name='图集价格', null=True)

    cover_img = models.ImageField(upload_to=create_album_folder)
    #和图集标签多对多的关系
    tags = models.ManyToManyField(to=AlbumTags, related_name='album_tags')

    #和Beauty多对一, 图集多,美女一
    beauty = models.ForeignKey(to=Beauty, on_delete=models.CASCADE, related_name='album')

    class Meta:
        ordering = ['-create_time']

    def get_uid(self):
       return self.uid

    def get_absolute_url(self):
        '''
        这里return语句,解析：内容很多
        （1）首先这个函数get_absolute_url就是针对每一个Album实体，返回一个绝对的URL，但是如何返回这个url，是一个学问
        或者说如何设计这个返回url的格式是问题，总的来说这个函数的功能是给每一个Album实体返回一个url。
        在return中返回的值，就是url的格式，这里有些内容可以自行设计，有些则不行：
        如：开头的/album --> 1.必不可少的是开头的反斜杠,因为在生产sitemaps.xml中产生的url跟这里保持一致，如果没有反斜杠就会变成127.0.0.1album域名和album中间没有隔开，这种url是不对的。
                            2.必不可少的是为什么要添加这个album，因为我们在这个app中的url.py中规定的app_name='album'如果这里不加上album，那么这个函数生产的url就缺失了album，那么就和url.py中规定的无法匹配
        如：/show_pic/ --> 这里也不是乱加的，是因为在views.py中有一个函数是查看详细的，同时这个函数指向的url.py中path里面也是这么定义的。所以需要搬过来。
        如：/%s/%s --> 这里也不是乱加的，还是和url中path里面有一个show_pic/<str:uid>/<str:str> 关联一起的。
        如：.html --> 这个是自己添加的，不添加也米有问题。

        （2）在这里构造了返回的绝对URL之后，那么在对应的模板HTML页面里面。如果需要用到album的实例，只需要直接调用 album.get_absolute_url这个函数就可以了，不需要在拼接路径。
        （3）系统里面其实还有一个叫slug的功能，其实也就是把标题转换成那种用 横杠- 链接的标题放到URL中去，这样在url中就可以看到当前访问的是什么。
            但是我们在这里没有用那个slug的功能，我们直接用标题当作url中的最后一个参数，因为是要用横杠代替空格，所以我们用self.title.replace()这个函数， 这里只处理一个空格的情况，其他的情况都没有处理
        '''
        return '/album/show_pic/%s/%s.html'%(self.uid, (self.title).replace('/','_').replace(' ','-'))





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