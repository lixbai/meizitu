from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from .models import NewsCategory, News
from utils import restful
from .serializers import  NewsSerializer
from meizitu import settings

# 表头的search功能
def search(request):
    query = request.POST.get('query')
    # 利用query来匹配名字，然后返回指定的女神
    print(query)
    return HttpResponse(query)


def download(request):
    return render(request, 'download/download_list.html')




# 主页视图
def news_index(request):
    # count 是一页几条新闻的意思
    count = settings.ONE_PAGE_NEWS_COUNT
    news = News.objects.prefetch_related('category','tag')[0:count]

    context = {
        'newses':news,
    }
    return render(request, 'news/news_index.html', context=context)

# 根据传递进来的category_name 选择返回对应的文章
def get_news_by_category(request):
    category_id = int(request.GET.get('category_id'), 0)
    # print(category_id)
    #在数据库中查找
    category = NewsCategory.objects.get(pk=category_id)
    # print(category.name)
    newses = News.objects.filter(category__id = category_id)
    # print(newses)
    ser = NewsSerializer(newses, many=True)
    # print(ser.data)
    return restful.result(data=ser.data)

# 根据传递进来的category和page 选择返回对应的文章
def news_list(request):
    # 通过p参数，来指定要获取第几页的数据
    # 并且这个p参数，是通过查询字符串的方式传过来的/news/list/?p=2
    page = int(request.GET.get('p',1))
    print(page)
    # 分类为0：代表不进行任何分类，直接按照时间倒序排序
    category_id = int(request.GET.get('category_id',0))
    # 0,1
    # 2,3
    # 4,5
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:
        # QuerySet
        # {'id':1,'title':'abc',category:{"id":1,'name':'热点'}}
        newses = News.objects.prefetch_related('category', 'tag').all()[start:end]
    else:
        newses = News.objects.prefetch_related('category', 'tag').filter(category__id=category_id)[start:end]
    serializer = NewsSerializer(newses,many=True)
    data = serializer.data
    print(data)
    return restful.result(data=data)

# 消息详情也展示
def news_detail(request, news_id):
    #根据传递进来的news_id 索引具体的news ,然后展示回去
    try:
        news = News.objects.get(pk=news_id)
    except:
        return render(request, '404.html')
    side_newses = News.objects.all()[0:10]
    context = {
        'news':news,
        'side_newses':side_newses
    }
    return render(request, 'news/news_detail.html', context=context)








