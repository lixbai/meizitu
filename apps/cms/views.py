from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required #装饰器，判断是不是 staff是的话，就让访问该视图
from django.views.generic import View
from django.views.decorators.http import require_POST
from apps.album.models import AlbumTags, Album, Pic
from apps.beauty.models import Beauty, BeautyTags
from utils import restful
from .forms import AlbumTagsForm, DelAlbumTagsForm
import os
from django.conf import settings


from utils.tencent_cos import client

#后台首页
@staff_member_required(login_url='/') #函数内部是重定向，如果不满足是staff的条件，就跳转到首页
def index(request):
    return render(request, 'cms/index.html')

'''
处理图集标签
'''
#处理图集标签页面的视图
class WriteAblumTagView(View):
    def get(self, request, *args, **kwargs):
        tags = AlbumTags.objects.all()
        context = {
            'tags': tags
        }
        return render(request, 'cms/manage_album_tags.html', context=context)

    # 增加标签视图
    def post(self, request, *args, **kwargs):
        # 把前台传递过来的数据，添加到数据库就可以了，当然还需要校验数据的正确性。因为AlbumTags只有一个数据，也可以不用使用那种表单的形式
        tag = request.POST.get ('tag')

        #前台传递过来的标签是一个大的字符串，各个标签之间用空格做分割，这里采用split()函数来做分割
        #分割成一个一个的标签，然后在分次存入数据库中，这样就避免了，前台一个一个的传递近来了。
        tag_list = str.split(tag)

        for i in range(len(tag_list)):
            try:
                # 校验传递过来的name是不是已经在数据库里面存在了，如果存在就不用插入了
                exists = AlbumTags.objects.filter (tag__icontains=tag_list[i]).exists ()

                if not exists:
                    AlbumTags.objects.create (tag=tag_list[i])
                else:
                    i = i + 1
            except:
                return restful.params_error (message='插入的有问题！')

        return restful.ok()


# 编辑图集标签视图
#因为是修改，所以需要一个索引，需要知道是哪一个要修改，还有要修改的值，一共需要传递两个值过来，所以需要用到post，所以需要用到表单
@require_POST
def edit_album_tags(request):
    form = AlbumTagsForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        tag = form.cleaned_data.get('tag')

        try:
            AlbumTags.objects.filter(pk=pk).update(tag=tag)
            return restful.ok()
        except:
            return restful.params_error(message='传入的数据有问题！')
    else:
        return restful.params_error(message=form.get_error())

# 删除图集标签视图
@require_POST
def del_album_tags(request):
    form = DelAlbumTagsForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
    try:
        t = AlbumTags.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.params_error(message='无法删除')


# ueditor 上传图片的处理视图.
@require_POST
def upload_files(request):
    #先从发送过来的request中获取文件,然后保存到本地
    file = request.FILES.get('file') #get()函数里面的file是ajax发送过来的名字.
    #获取file的名字
    name = file.name
    #保存, 注意这里open的第一个参数,是一个拼接的路径,
    with open(os.path.join(settings.MEDIA_ROOT,name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)

    #这里需要获取上传的文件的具体路径,所以需要用requst里面的一个方法get_absulate_uri()来拼接具体的完整路径,
    # 拼接成完成的绝对路径如: http://127.0.0.1/media/xxx.jpg的形式
    url = request.build_absolute_uri(settings.MEDIA_URL+name) #注意参数里面其实是两个参数的字符串叠加,settings.MEDIA_URL是setting文件里面设置的/media/,加上文件名字namejiu可以了
    #把上面拼接得到的完整的路径返回给js,燃js在现实在那个输入框里面.
    return restful.result(data={'url':url})


'''
处理美女标签
'''
# 处理美女标签的视图
class WriteBeautyTagView(View):
    def get(self, request, *args, **kwargs):
        tags = BeautyTags.objects.all()
        context = {
            'tags': tags
        }
        return render(request, 'cms/manage_beauty_tags.html', context=context)

    #处理新增标签的功能
    def post(self, request, *args, **kwargs):
        #获取前台传递过来的tag,检查之后存入数据库,这个是用JS传递过来的,
        tag = request.POST.get('tag')
        print(tag)
        #利用split 函数来隔断传递进来的字符串
        tag_list = str.split(tag)
        print(tag_list)
        for i in range(len(tag_list)):
            try:
                #检查这个tag是不是已经存在
                exists = BeautyTags.objects.filter(tag__icontains=tag_list[i]).exists()
                if not exists:
                    BeautyTags.objects.create(tag=tag_list[i])
                else:
                    i = i + 1
            except:
                return restful.params_error('插入出现问题！')
        return restful.ok()

#定义修改美女标签的视图
@require_POST
def edit_beauty_tag(request):
    #这里让人采用的是JS,向服务器发送数据
    #这里暂时不用form表单的形式,看下直接获取OK不
    pk = request.POST.get('pk')
    tag = request.POST.get('tag')
    #这里其实根本不用做重复性判断,因为无论老的值和新的值是否一样,都做插入处理.

    try:
        BeautyTags.objects.filter(pk=pk).update(tag=tag)
        return restful.ok()
    except:
        return restful.params_error(message='无法修改')

#定义删除美女标签的功能
@require_POST
def delete_beauty_tag(request):
    #根据js传递过来的标签的id,到数据库中执行删除操作
    pk = request.POST.get('pk')
    print(pk)
    try:
        BeautyTags.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.params_error(message='无法删除!')



'''
处理美女
'''
#处理美女的视图
class WriteBeautyView(View):
    def get(self, request, *args, **kwargs):
        tags = BeautyTags.objects.all()
        context = {
            'tags':tags
        }
        return render(request, 'cms/manage_beauty.html', context=context)

    # 增加美女
    # 这里没有用form
    def post(self, request, *args, **kwargs):
        beauty_name = request.POST.get('beauty_name')
        age = request.POST.get('age')
        birthday = request.POST.get('birthday')
        country = request.POST.get('country')
        xingzuo = request.POST.get('xingzuo')
        tall = request.POST.get('tall')
        weight =request.POST.get('weight')
        sanwei = request.POST.get('sanwei')
        job = request.POST.get('job')
        interested = request.POST.get('interested')
        detail = request.POST.get('detail')
        cover_img = request.FILES.get('cover_img')

        # 处理tags,获得前台选中的tags的实体instance,是多个
        tags_id = request.POST.getlist('tags')
        #定义一个列表,然后吧tags_id中的数字,一个一个的找出对应的Tags,然后统一和则合格beauty instance关联
        upload_beauty_tags = []
        for i in range(len(tags_id)):
            upload_beauty_tags.append(
                BeautyTags.objects.get(pk=int(tags_id[i]))
        )

        print('*'*20)
        print(beauty_name, age, birthday, country, xingzuo, tall, weight, sanwei, job, interested, detail, cover_img, tags_id)
        print('*'*20)

        try:
            beauty = Beauty.objects.create(beauty_name=beauty_name, age=age, birthday=birthday, country=country, xingzuo=xingzuo, tall=tall, weight=weight, sanwei=sanwei, job=job, interested=interested, detail=detail, cover_img=cover_img)

            #多对多添加
            beauty.tags.add(*upload_beauty_tags)
            # return restful.ok()
            return redirect('cms:write_beauty')
        except:
            return restful.params_error('美女信息插入不成功!')



'''
处理图集
'''
# class WriteAlbumView(View):
#     def get(self, request, *args, **kwargs):
#         tags = AlbumTags.objects.all()
#         #暂时是吧所有的女神的资料都在这里返回,但是如果系统里面女神较多,可以例用JS把前面传递的,在单独的函数里面返回.
#
#         beautys = Beauty.objects.all()
#         context = {
#             'tags':tags,
#             'beautys': beautys
#         }
#         return render(request, 'cms/manage_album.html', context=context)
#
#     #新增图集
#     def post(self, request,*args, **kwargs):
#         watch_count = request.POST.get('watch_count')
#         title = request.POST.get('title')
#         desc = request.POST.get('desc')
#         beauty_name = request.POST.get('beauty_name')
#         download_url = request.POST.get('download_url')
#         download_password = request.POST.get('download_password')
#         download_price = request.POST.get('download_price')
#
#         cover_img = request.FILES.get('cover_img')
#
#         #获取多个标签,这里tags_id是数组,
#         tags_id = request.POST.getlist('tags')
#         album_tags_list = []
#         for i in range(len(tags_id)):
#             album_tags_list.append(
#                 AlbumTags.objects.get(pk=int(tags_id[i]))
#             )
#
#         #获取传递过来的beauty
#         beauty_id = request.POST.get('beauty')
#         beauty = Beauty.objects.get(pk=beauty_id)
#
#         print('*'*30)
#         print(watch_count,title, desc, beauty_name, download_url, download_password, download_price, cover_img, tags_id, beauty_id)
#         print(beauty)
#         print('download_price', download_price)
#         print(album_tags_list)
#         print('*'*30)
#
#         try:
#             #把数据插入
#             a = Album.objects.create(cover_img=cover_img, watch_count=watch_count, title=title, desc=desc, beauty_name=beauty_name, download_url=download_url,download_password=download_password, download_price=download_price, beauty=beauty)
#             #标签和图集多对多插入
#             a.tags.add(*album_tags_list)
#             print('uid...->',a.get_uid())
#             print(cover_img.name)
#             s_path=os.path.join(settings.MEDIA_ROOT,'album',a.get_uid(),cover_img.name)
#
#             # print(os.listdir(path))
#
#             d_file_path = os.path.join('album',a.get_uid(),cover_img.name).replace('\\','/')
#             print(d_file_path)
#
#             # 上传到腾讯Cos
#             r = client.put_object_from_local_file (
#                 Bucket='li-1302251434',
#                 LocalFilePath=s_path,
#                 Key=d_file_path,
#             )
#             print (r ['ETag'])
#
#             #上传到阿里云OSS
#             from utils.aliyun_oss import bucket
#             res = bucket.put_object_from_file(d_file_path, s_path)
#             print('aliyun-------->', res.status)
#
#
#             # # 高级上传接口(推荐)
#             # r = client.upload_file (
#             #     Bucket='li-1302251434',
#             #     LocalFilePath=s_path,
#             #     Key=d_file_path,
#             #     PartSize=10,
#             #     MAXThread=10,
#             #
#             # )
#             # print (r['ETag'])
#
#             return redirect('cms:write_album')
#         except:
#             return restful.params_error('插入图集数据不成功')




'''
处理图集 和 图片一起上传
'''
class WriteAlbumView(View):
    def get(self, request, *args, **kwargs):
        tags = AlbumTags.objects.all()
        #暂时是吧所有的女神的资料都在这里返回,但是如果系统里面女神较多,可以例用JS把前面传递的,在单独的函数里面返回.

        beautys = Beauty.objects.all()
        context = {
            'tags':tags,
            'beautys': beautys
        }
        return render(request, 'cms/manage_album_pic.html', context=context)

    #新增图集 和 图片
    def post(self, request,*args, **kwargs):
        watch_count = request.POST.get('watch_count')
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        beauty_name = request.POST.get('beauty_name')
        download_url = request.POST.get('download_url')
        download_password = request.POST.get('download_password')
        download_price = request.POST.get('download_price')

        cover_img = request.FILES.get('cover_img')

        # 上传图片集合
        pictures = request.FILES.getlist ('picture')

        #获取多个标签,这里tags_id是数组,
        tags_id = request.POST.getlist('tags')
        album_tags_list = []
        for i in range(len(tags_id)):
            album_tags_list.append(
                AlbumTags.objects.get(pk=int(tags_id[i]))
            )

        #获取传递过来的beauty
        beauty_id = request.POST.get('beauty')
        beauty = Beauty.objects.get(pk=beauty_id)

        print('*'*30)
        print(watch_count,title, desc, beauty_name, download_url, download_password, download_price, cover_img, tags_id, beauty_id)
        print(beauty)
        print('download_price', download_price)
        print(album_tags_list)
        print('*'*30)

        try:
            #把数据插入
            a = Album.objects.create(cover_img=cover_img, watch_count=watch_count, title=title, desc=desc, beauty_name=beauty_name, download_url=download_url,download_password=download_password, download_price=download_price, beauty=beauty)
            #标签和图集多对多插入
            a.tags.add(*album_tags_list)

            #上传图片
            try:
                # 创建多个pic实例，然后同意保存到数据库，用于接收前台传入的多个文件

                # 先创建一个列表
                more_pic_list = []
                # 创建多个实例：
                for i in range (int (len (pictures))):
                    more_pic_list.append (
                        Pic (
                            picture=pictures [i], album=a
                        )
                    )

                if more_pic_list:
                    try:
                        # Pic.objects.create(picture=pic, album=a)
                        Pic.objects.bulk_create (more_pic_list)

                        # 上传cover_img 到阿里云 腾讯云
                        print ('uid...->', a.get_uid ())
                        print ('cover_img.name...->', cover_img.name)
                        src_cover_img_path = os.path.join (settings.MEDIA_ROOT, 'album', a.get_uid (), cover_img.name)
                        dest_cover_img_path = os.path.join ('album', a.get_uid (), cover_img.name).replace ('\\', '/')
                        print ('dest_cover_img_path-->',dest_cover_img_path)

                        # 上传cover_img到腾讯Cos
                        r = client.put_object_from_local_file (
                            Bucket='li-1302251434',
                            LocalFilePath=src_cover_img_path,
                            Key=dest_cover_img_path,
                        )
                        print (r ['ETag'])

                        # 上传cover_img到阿里云OSS
                        from utils.aliyun_oss import bucket
                        res = bucket.put_object_from_file (dest_cover_img_path, src_cover_img_path)
                        print ('aliyun-------->', res.status)


                        # 上传图片Pic 到阿里云 腾讯云
                        src_pic_path_dir = os.path.join (settings.MEDIA_ROOT, 'pic', a.get_uid ())
                        print(src_pic_path_dir)
                        name_list = os.listdir(src_pic_path_dir)
                        print(name_list)

                        # 循环添加图片到云空间
                        for i in range(len(name_list)):
                            # 上传到阿里云
                            bucket.put_object_from_file(
                                os.path.join('pic', a.get_uid(), name_list[i]).replace('\\', '/'),
                                os.path.join(settings.MEDIA_ROOT, 'pic', a.get_uid(), name_list[i])
                            )
                            # 上传到腾讯云
                            client.put_object_from_local_file(
                                Bucket='li-1302251434',
                                LocalFilePath=os.path.join(settings.MEDIA_ROOT, 'pic', a.get_uid(), name_list[i]),
                                Key=os.path.join('pic', a.get_uid(), name_list[i]).replace('\\', '/')
                            )

                        return HttpResponse('图片上传成功!')
                    except:
                        return HttpResponse ('图片上传不成功')
                else:
                    return HttpResponse ('图片上传有问题！！！')
            except:
                return restful.params_error ('上传图片不成功')
            # return redirect('cms:write_album')
        except:
            return restful.params_error('插入图集数据不成功')







'''
处理图集对应的图片
'''

class PicView(View):
    def get(self, request, *args, **kwargs):
        albums = Album.objects.all()
        context = {
            'albums':albums
        }
        return render(request, 'cms/manage_pic.html', context=context)

    #新增图片
    def post(self, request, *args, **kwargs):
        album_id = request.POST.get('album')
        album = Album.objects.get(pk=album_id)

        pictures = request.FILES.getlist('picture')

        print('*'*30)
        print(album_id, album, pictures)
        print('*'*30)

        try:
            # 创建多个pic实例，然后同意保存到数据库，用于接收前台传入的多个文件

            # 先创建一个列表
            more_pic_list = []
            # 创建多个实例：
            for i in range (int (len (pictures))):
                more_pic_list.append (
                    Pic (
                        picture=pictures [i], album=album
                    )
                )

            if more_pic_list:
                try:
                    # Pic.objects.create(picture=pic, album=a)
                    Pic.objects.bulk_create (more_pic_list)
                    return redirect('cms:write_pic')
                except:
                    return HttpResponse ('图片上传不成功')

            else:
                return HttpResponse ('有问题！！！')

        except:
            return restful.params_error('上传图片不成功')
