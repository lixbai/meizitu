from django.db import models

# 广告分类
class AdCategory(models.Model):
    ad_category_name = models.CharField(max_length=30)

'''
广告位表（广告位编号，分类编号，广告位名称，价格，格式，描述，状态（开启，关闭））
'''
# 广告
class Ad(models.Model):
    title = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    desc =models.CharField(max_length=500, null=True)
    thumbnail = models.URLField(null=True)
    state = models.BooleanField(default=False)
    ad_category = models.ForeignKey(to=AdCategory, on_delete=models.CASCADE,related_name='ad')

'''
广告位记录表（记录编号，广告位编号，类型（有图片，flash）,URL，开始时间，结束时间）
'''
# 广告记录表
class AdRecord(models.Model):
    ad = models.ForeignKey(to=Ad, on_delete=models.CASCADE, related_name='ad_record')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
