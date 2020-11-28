from django.shortcuts import render
from django.http import HttpResponse
from .models import AlbumTags, Album
from apps.beauty.models import BeautyTags
from django.conf import settings
from django.views.generic import View
from django.core.paginator import Paginator
from django.db import connection
from utils.aliyun_oss import a_prefix_url
from utils.tencent_cos import t_prefix_url

def index(request):
    # beauty_tags = BeautyTags.objects.all()
    #
    # context = {
    #     'beauty_tags':beauty_tags
    # }
    # 这里实际上需要用到分页，但是分页后面在做
    albums = Album.objects.all ()
    url = request.build_absolute_uri (settings.MEDIA_URL)

    context = {
        'albums': albums,
        't_prefix_url': t_prefix_url
    }


    return render(request, 'album/index-bak2.html', context=context)

# album 主页
# def albums(request):
#     # 这里实际上需要用到分页，但是分页后面在做
#     albums = Album.objects.all()
#     url = request.build_absolute_uri(settings.MEDIA_URL)
#
#     context = {
#         'albums': albums,
#         'url': url
#     }
#     return render(request, 'album/beauty_album.html', context=context)

# album 主页
class AlbumsView(View):
    def get(self, request):
        page = int (request.GET.get ('p', 1))
        # 这里实际上需要用到分页，但是分页后面在做
        albums = Album.objects.all()
        url = request.build_absolute_uri (settings.MEDIA_URL)

        #做分页处理
        paginator = Paginator (albums, 2)
        page_obj = paginator.page (page)

        context_data = self.get_pagination_data (paginator, page_obj)

        context = {
            'albums': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,

            'url': url,
            'a_prefix_url': a_prefix_url,
            't_prefix_url': t_prefix_url
        }
        context.update(context_data)
        return render (request, 'album/beauty_album.html', context=context)

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


def tags_get_beauty(request):
    #利用id来寻找到对应的beautyTags,然后利用这个beautyTags来找到对应的Beauty
    pk = request.GET.get('p')
    print('pk===', pk)
    bts = BeautyTags.objects.get(pk=pk)
    print('bts===', bts)
    ball = bts.beauty.all()
    print('ball===', ball)

    return HttpResponse(bts.tag)


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
class TagGetAlbumView(View):
    def get(self, request, tag, *args, **kwargs):
        #获取传递进来的分页的标志,默认第一页
        page = int(request.GET.get('p', 1))

        albumtag = AlbumTags.objects.prefetch_related('album_tags').get(pk=tag)
        # albumtag = AlbumTags.objects.get(pk=tag)
        # 根据albumTags的实例对象，查找管理的album对象，manytomany的关系
        albums = albumtag.album_tags.all()

        url = request.build_absolute_uri(settings.MEDIA_URL)

        #做分页处理
        paginator = Paginator(albums, 2)
        page_obj = paginator.page(page)
        #例用这个函数处理分页
        context_data = self.get_pagination_data(paginator, page_obj)

        context = {
            'tag':albumtag.tag,
            'albums': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'url':url
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
def show_pic(request, uid):
    #根据uid 可以查到album中的数据,同时还可以查到pic表中的数据,因为这个uid在两个表中都存在

    # 1,先差album, 把其中需要传递的数据先拿出来,这个暂时不做那个优化
    # album = Album.objects.get(pk=uid)
    album = Album.objects.prefetch_related('tags', 'pic').get(pk=uid)

    # tags = album.tags.all()
    # pics = album.pic.all()

    url = request.build_absolute_uri (settings.MEDIA_URL)

    context = {
        'album':album,
        'tags': album.tags.all(),
        'pics': album.pic.all(),
        'url': url,
        't_prefix_url':t_prefix_url
    }

    return render(request, 'album/pic_show.html', context=context)



# 表头的search功能
def search(request):
    query = request.POST.get('query')
    # 利用query来匹配名字，然后返回指定的女神
    print(query)
    return HttpResponse(query)
