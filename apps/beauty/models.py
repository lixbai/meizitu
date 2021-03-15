from django.db import models
import os
from shortuuidfield import ShortUUIDField

# 美女tags
class BeautyTags(models.Model):
    tag = models.CharField(max_length=30)


#定义存放美女封面图片的路径
#这里单独吧美女封面的路径为: /media/beauty/uid/xx.jpg
#因为这里后台是我们自己再用,所以知道上传的是图片,不用做校验,如果是开放的系统,这里需要做图片类型的校验~!
def create_beauty_folder(insance, filename):
    return os.path.join('beauty/', insance.uid, filename)

# 美女项目
class Beauty(models.Model):
    '''
    封面img	美女tags	姓名	年 龄	生 日	星 座	身 高	体 重	三 围	出 生	职 业	兴 趣	创建时间	修改时间
            多对多
    '''
    # 主键用shortuuid来做,
    uid = ShortUUIDField(primary_key=True)

    beauty_name = models.CharField(max_length=40)
    age = models.CharField(max_length=20, null=True)
    birthday = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=50, null=True)
    xingzuo = models.CharField(max_length=30, null=True)
    tall = models.CharField(max_length=20, null=True)
    weight = models.CharField(max_length=20, null=True)
    sanwei = models.CharField(max_length=40, null=True)
    job = models.CharField(max_length=30, null=True)
    interested = models.CharField(max_length=100, null=True)
    detail = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    # 存放图片的
    cover_img = models.ImageField (upload_to=create_beauty_folder)

    # 和标签多对多类型
    tags = models.ManyToManyField(to=BeautyTags, related_name='beauty')

    class Meta:
        ordering = ['-create_time']


    def get_uid(self):
       return self.uid

