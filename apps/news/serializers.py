from rest_framework import serializers
from .models import NewsCategory, News

class NewsSerializer(serializers.ModelSerializer):
    # 不使用depth=1的时候，需要对category这个多对多的属性进行获取name值的操作，这里就用到了函数来做。
    # category = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = ('id','title', 'desc', 'thumbnail', 'pub_time', 'category', 'tag')
        depth = 1

    # 不使用depth=1的时候，需要对category这个多对多的属性进行获取name值的操作，这里就用到了函数来做。
    # 如果使用了depth=1这个操作，就不需要在单独对多对多进行函数操作了，系统自己会完成操作。
    # def get_category(self, n):
    #     category_list = n.category.all()
    #     print(category_list)
    #     ret = []
    #     for item in category_list:
    #         ret.append({'id':item.pk, 'name':item.name})
    #     return ret
