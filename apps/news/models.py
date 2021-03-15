from django.db import models


class NewsCategory (models.Model):
    name = models.CharField (max_length=100)


class NewsTag (models.Model):
    tag = models.CharField (max_length=30)


class News (models.Model):
    title = models.CharField (max_length=200)
    desc = models.CharField (max_length=200, null=True)
    thumbnail = models.URLField ()
    content = models.TextField ()
    pub_time = models.DateTimeField (auto_now_add=True)
    # 分类板块
    category = models.ManyToManyField ('NewsCategory', related_name='news_category')
    # 文章的标签
    tag = models.ManyToManyField ('NewsTag', related_name='news_tag')

    class Meta:
        ordering = ['-pub_time']

# class Comment (models.Model):
#     content = models.TextField ()
#     pub_time = models.DateTimeField (auto_now_add=True)
#     news = models.ForeignKey ("News", on_delete=models.CASCADE, related_name='comments')
#
#     class Meta:
#         ordering = ['-pub_time']
