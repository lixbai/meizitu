from django.db import models

class NewsCategory (models.Model):
    name = models.CharField (max_length=100)

class NewsTag (models.Model):
    tag = models.CharField (max_length=30)

class News (models.Model):
    title = models.CharField (max_length=300)
    desc = models.CharField (max_length=500, null=True)
    thumbnail = models.URLField ()
    content = models.TextField ()
    pub_time = models.DateTimeField (auto_now_add=True)
    # 分类板块
    category = models.ManyToManyField ('NewsCategory', related_name='news_category')
    # 文章的标签
    tag = models.ManyToManyField ('NewsTag', related_name='news_tag')

    class Meta:
        ordering = ['-pub_time']

    def get_absolute_url(self):
        '''
        注意这里：跟album和beauty 里面不一样，这里没有对标题进行处理，按照一般想，这样应该是不行的，因为有可能title里面有字符不符合url的规定，
        那么为什么在这里还这样不作处理，直接用哪？
        因为我们在url.py中对标题的部分使用的 转换器是 path 而不是str, 使用path转换器，就不需要在这里进行处理。
        '''
        return '/news/detail/%s/%s'%(self.pk, self.title)

# class Comment (models.Model):
#     content = models.TextField ()
#     pub_time = models.DateTimeField (auto_now_add=True)
#     news = models.ForeignKey ("News", on_delete=models.CASCADE, related_name='comments')
#
#     class Meta:
#         ordering = ['-pub_time']
