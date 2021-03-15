from django.shortcuts import render
from .models import BeautyTags, Beauty
from apps.news.models import News
from django.views.generic import View
from django.conf.urls.static import settings
from django.core.paginator import Paginator, Page
from django.utils import timezone
import random
from rest_framework.views import APIView
from utils.throttle import VisitThrottle
from rest_framework.renderers import JSONRenderer

#封装, 把分页算法单独提出来一个类中,然后下面用继承来做
class MyPaginatorMixin(object):
    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range (1, current_page)
        else:
            left_has_more = True
            left_pages = range (current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range (current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range (current_page + 1, current_page + around_count + 1)

        return {
            # left_pages：代表的是当前这页的左边的页的页码
            'left_pages': left_pages,
            # right_pages：代表的是当前这页的右边的页的页码
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }

#改写美女首页,用分页
class BeautyView(APIView, MyPaginatorMixin):
    throttle_classes = [VisitThrottle,]
    renderer_classes = [JSONRenderer]
    def get(self, request, *args, **kwargs):
        #根据分页的标志p,来获取是第几页
        page = int(request.GET.get('p', 1))
        try:
            beautys = Beauty.objects.prefetch_related('album').all()
        except:
            return render(request, '404.html')

        url = request.build_absolute_uri(settings.MEDIA_URL)

        # 这里做一个猜你喜欢的女神的功能 开始
        # 思路同样是：获取点击时候的创建时间，然后用一个随机的天数，这样每一次调用这个函数都是不一样的返回结果
        random_days = timezone.now () + timezone.timedelta (days=random.randint (-60, -8))
        random_beautys = beautys.filter (create_time__lt=random_days)[0:5]
        # 这里做一个猜你喜欢的女神的功能 结束

        #作分页处理
        paginator = Paginator(beautys, 30)
        page_obj = paginator.page(page)

        page_data = self.get_pagination_data(paginator, page_obj)

        context = {
            'beautys': page_obj.object_list,
            'page_obj':page_obj,
            'paginator': paginator,

            'url': url,
            'random_beautys': random_beautys
        }
        context.update(page_data)
        return render(request, 'beauty/beauty.html', context=context)


#根据传递进来的tag, 获取关联的图集beauty, 方法1:不用分页
def tags(request, tag):
    # albumtag = AlbumTags.objects.prefetch_related('album_tags').get(pk=tag)

    beautytag = BeautyTags.objects.get (pk=tag)
    # 根据albumTags的实例对象，查找管理的album对象，manytomany的关系
    beautys = beautytag.beauty.all()

    url = request.build_absolute_uri (settings.MEDIA_URL)
    print (url)

    context = {
        'tag': beautytag.tag,
        'beautys': beautys,
        'url': url
    }
    return render (request, 'beauty/tags_get_beauty.html', context=context)

#根据传递进来的tag, 获取关联的图集beauty, 方法2:用分页
class TagGetBeautyView(APIView, MyPaginatorMixin):
    throttle_classes = [VisitThrottle,]
    def get(self, request, tag, *args, **kwargs):
        #因为是用分页,所以需要传递进来参数标志p,如果没有,就默认第一页,
        page = int(request.GET.get('p', 1))

        # 注意下面的'beauty__album' 这个设定，这个用双下划线关联第三张表
        try:
            beautytag = BeautyTags.objects.prefetch_related('beauty','beauty__album').get (pk=tag)
            # 根据albumTags的实例对象，查找管理的album对象，manytomany的关系
            # beautys = beautytag.beauty.all()
            beautys = beautytag.beauty.all()
        except:
            return render(request, '404.html')

        url = request.build_absolute_uri (settings.MEDIA_URL)

        # 这里做一个猜你喜欢的女神的功能 开始
        # 思路同样是：获取点击时候的创建时间，然后用一个随机的天数，这样每一次调用这个函数都是不一样的返回结果
        random_days = timezone.now () + timezone.timedelta (days=random.randint (-60, -8))
        random_beautys = Beauty.objects.filter (create_time__lt=random_days) [0:5]
        # 这里做一个猜你喜欢的女神的功能 结束

        #处理分页
        paginator = Paginator(beautys, 24)
        page_obj = paginator.page(page)

        page_data = self.get_pagination_data(paginator, page_obj)

        context = {
            'tag': beautytag.tag,
            'beautys': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'url': url,
            'random_beautys': random_beautys
        }
        context.update(page_data)
        return render (request, 'beauty/tags_get_beauty.html', context=context)


class BeautyDetailView(APIView):
    throttle_classes = [VisitThrottle]
    def get(self, request, uid, *args, **kwargs):
        # 根据uid 查找对应的instance,
        try:
            beauty = Beauty.objects.prefetch_related ('album').get (pk=uid)
            # 根据这个beauty 查找出所有的图集
            beauty_albums = beauty.album.all ()
        except:
            return render (request, '404.html')

        # 这里做一个猜你喜欢的女神的功能 开始
        # 思路同样是：根据上面UID获取到的beauty，获取这个实例的创建时间，然后用一个随机的天数，这样每一次调用这个函数都是不一样的返回结果
        random_days = beauty.create_time + timezone.timedelta (days=random.randint (-30, -8))
        random_beautys = Beauty.objects.filter (create_time__lt=random_days) [0:5]
        # 这里做一个猜你喜欢的女神的功能 结束

        url = request.build_absolute_uri (settings.MEDIA_URL)

        context = {
            'beauty': beauty,
            'beauty_albums': beauty_albums,
            'url': url,

            'random_beautys': random_beautys,
        }

        return render (request, 'beauty/beauty_detail.html', context=context)



def beauty_detail(request, uid):
    #根据uid 查找对应的instance,
    try:
        beauty = Beauty.objects.prefetch_related('album').get(pk=uid)
        #根据这个beauty 查找出所有的图集
        beauty_albums = beauty.album.all()
    except:
        return render(request, '404.html')

    # 这里做一个猜你喜欢的女神的功能 开始
    # 思路同样是：根据上面UID获取到的beauty，获取这个实例的创建时间，然后用一个随机的天数，这样每一次调用这个函数都是不一样的返回结果
    random_days = beauty.create_time + timezone.timedelta(days=random.randint(-30, -8))
    random_beautys = Beauty.objects.filter(create_time__lt=random_days)[0:5]
    # 这里做一个猜你喜欢的女神的功能 结束

    url = request.build_absolute_uri(settings.MEDIA_URL)

    context = {
        'beauty':beauty,
        'beauty_albums':beauty_albums,
        'url':url,

        'random_beautys':random_beautys,
    }

    return render(request, 'beauty/beauty_detail.html', context=context)