from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required #装饰器，判断是不是 staff是的话，就让访问该视图
from django.views.generic import View
from django.views.decorators.http import require_POST, require_GET
from apps.album.models import AlbumTags, Album, Pic
from apps.beauty.models import Beauty, BeautyTags
from utils import restful
from .forms import AlbumTagsForm, DelAlbumTagsForm, BeautyForm
import os,datetime
from django.conf import settings

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
        # 校验传递过来的name是不是已经在数据库里面存在了，如果存在就不用插入了
        exists = AlbumTags.objects.filter (tag__icontains=tag).exists ()

        if not exists:
            AlbumTags.objects.create (tag=tag)
            return restful.ok ()
        else:
            return restful.params_error (message='插入的标签已经存在数据库中！')


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
        #检查这个tag是不是已经存在
        exists = BeautyTags.objects.filter(tag__icontains=tag).exists()

        if not exists:
            BeautyTags.objects.create(tag=tag)
            return restful.ok()
        else:
            return restful.params_error(message='插入的标签已经存在')

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

    #增加美女
    #这里没有用form
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

        try:
            beauty = Beauty.objects.create(beauty_name=beauty_name, age=age, birthday=birthday, xingzuo=xingzuo, tall=tall, weight=weight, sanwei=sanwei, job=job, interested=interested, detail=detail, cover_img=cover_img)

            #多对多添加
            beauty.tags.add(*upload_beauty_tags)
            return restful.ok()
        except:
            return restful.params_error('美女信息插入不成功!')



