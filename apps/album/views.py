from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import AlbumTags, Album
from apps.beauty.models import BeautyTags
from django.conf import settings
from django.views.generic import View
from django.core.paginator import Paginator
# from utils.aliyun_oss import a_prefix_url
# from utils.tencent_cos import t_prefix_url
import random
import json
from django.utils import timezone
from rest_framework.views import APIView
from utils.throttle import VisitThrottle
from rest_framework.renderers import JSONRenderer,TemplateHTMLRenderer

# album 主页
class AlbumsView(APIView):
    #这里做限流措施
    throttle_classes = [VisitThrottle,]
    renderer_classes = [JSONRenderer]

    def get(self, request):
        page = int (request.GET.get ('p', 1))
        try:
            albums = Album.objects.all()
        except:
            return render(request, '404.html')
        pre_url = request.build_absolute_uri (settings.MEDIA_URL)

        # 你可以感兴趣的功能 开始
        random_day = timezone.now() + timezone.timedelta(days=random.randint(-16, -8))
        random_albums = albums.filter(create_time__lt=random_day)[0:5]
        # 你可以感兴趣的功能 结束

        #做分页处理
        paginator = Paginator (albums, 16)
        page_obj = paginator.page (page)

        context_data = self.get_pagination_data (paginator, page_obj)

        context = {
            'albums': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,

            'url': pre_url,
            # 'a_prefix_url': a_prefix_url,
            # 't_prefix_url': t_prefix_url,
            'random_albums':random_albums
        }
        context.update(context_data)
        return render (request, 'album/album.html', context=context)

    def get_pagination_data(self,paginator,page_obj,around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1,current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count,current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page+1,num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1,current_page+around_count+1)

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


# #根据传递进来的tag, 获取关联的图集album
# def tags(request, tag):
#
#     # albumtag = AlbumTags.objects.prefetch_related('album_tags').get(pk=tag)
#
#     albumtag = AlbumTags.objects.get(pk=tag)
#     # 根据albumTags的实例对象，查找管理的album对象，manytomany的关系
#     albums = albumtag.album_tags.all()
#
#     url = request.build_absolute_uri(settings.MEDIA_URL)
#     print(url)
#
#     context = {
#         'tag':albumtag.tag,
#         'albums': albums,
#         'url':url
#     }
#     return  render(request, 'album/tags_get_album.html',context=context)

# 根据传递进来的tag,获取关联的图集album
class TagGetAlbumView(APIView):
    throttle_classes = [VisitThrottle,]
    renderer_classes = [JSONRenderer]
    def get(self, request, *args, **kwargs):
        #获取传递进来的分页的标志,默认第一页
        tag = kwargs['tag']
        page = int(request.GET.get('p', 1))

        try:
            albumtag = AlbumTags.objects.prefetch_related('album_tags').get(tag=tag)
        except:
            return render(request, '404.html')
        # albumtag = AlbumTags.objects.get(pk=tag)
        # 根据albumTags的实例对象，查找管理的album对象，manytomany的关系
        albums = albumtag.album_tags.all()

        pre_url = request.build_absolute_uri(settings.MEDIA_URL)

        # 你可能感兴趣的功能开始
        ctime = timezone.now()
        # 随机修改days
        random_day = ctime + timezone.timedelta(days=random.randint(-30, -16))
        random_albums = albums.filter(create_time__lt=random_day)[0:5]

        # 你可能感兴趣的功能结束

        #做分页处理
        paginator = Paginator(albums, 16)
        page_obj = paginator.page(page)
        #例用这个函数处理分页
        context_data = self.get_pagination_data(paginator, page_obj)

        context = {
            'tag':albumtag.tag,
            'albums': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'url':pre_url,

            'random_albums':random_albums
        }
        context.update(context_data)
        return render(request, 'album/tags_get_album.html',context=context)

    def get_pagination_data(self,paginator,page_obj,around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1,current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count,current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page+1,num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1,current_page+around_count+1)

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


# 点击就可以察看到pic_html
class ShowPicView(APIView):
    throttle_classes = [VisitThrottle,]
    renderer_classes = [JSONRenderer]
    def get(self, request, *args, **kwargs):
        # 根据uid 可以查到album中的数据,同时还可以查到pic表中的数据,因为这个uid在两个表中都存在
        uid = kwargs['uid']
        # 1,先差album, 把其中需要传递的数据先拿出来
        try:
            album = Album.objects.prefetch_related ('tags', 'pic').get(pk=uid)
            # tags = album.tags.all()
            pics = album.pic.all().order_by('pk')
        except:
            return render(request, '404.html')

        # 分页功能代码开始
        # 获取传递进来的分页的标志,默认第一页
        page = int (request.GET.get ('p', 1))
        # 做分页处理
        paginator = Paginator (pics, 5)
        page_obj = paginator.page (page)
        # 例用这个函数处理分页
        context_data = self.get_pagination_data (paginator, page_obj)
        # 分页功能代码结束

        pre_url = request.build_absolute_uri (settings.MEDIA_URL)

        '''
         点击 换一组的功能开始，这里用随机的功能吧
         这里用不了随机，因为主键是shortUUID类型，不是整形，不能用
         这里的思路是：首先获取当前album的创建时间，然后朝前面倒1个月，开始选择，然后显示
         1,你可能感兴趣的其他图集-->朝前面倒4-10天，开始选择5个，然后显示
         这里timedelta里面的days可以用随机数，这样点击就是随机的了，哈哈好机智
        '''
        # 用的系统时间,这里的timezone是aware_time
        # ctime = timezone.now ()
        ctime = album.create_time
        random_day = random.randint (-8, -4)  # 随机选择一个整数
        before_days = ctime + timezone.timedelta (days=random_day)
        random_albums = Album.objects.filter (create_time__lt=before_days) [0:5]
        # 猜你喜欢和热门图集代码结束
        context = {
            'album': album,
            'tags': album.tags.all (),
            'pics': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'url': pre_url,
            # 't_prefix_url': t_prefix_url,

            'random_albums': random_albums,
        }
        context.update(context_data)

        return render (request, 'album/pic_show.html', context=context)

    # 分页函数代码
    def get_pagination_data(self,paginator,page_obj,around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1,current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count,current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page+1,num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1,current_page+around_count+1)

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

# 点击 换一组的功能，这里用随机的功能吧
# 这里用不了随机，因为主键是shortUUID类型，不是整形，不能用
# 这里的思路是：首先获取当前时间，然后朝前面倒1个月，开始选择5个，然后显示
def random_album(request):
    # 用的系统时间,这里的timezone是aware_time
    ctime = timezone.now()
    print(ctime)
    before_30_day = ctime + timezone.timedelta(days=-30)
    print(before_30_day)

    album_12 = Album.objects.filter(create_time__lt=before_30_day)[0:13]
    print(album_12)

    return HttpResponse(ctime)

