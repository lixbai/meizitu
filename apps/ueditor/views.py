#encoding: utf-8
import json
import re
import string
import time
import hashlib
import random
import base64
import sys
import os
from urllib import parse
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from meizitu import settings as meizitu_settings


# 更改工作目录。这么做的目的是七牛qiniu的sdk
# 在设置缓存路径的时候默认会设置到C:/Windows/System32下面
# 会造成没有权限创建。
os.chdir(os.path.dirname(__file__))
try:
    import qiniu
except:
    pass

# 上传到阿里云
try:
    import oss2
except:
    pass

from io import BytesIO


UEDITOR_QINIU_ACCESS_KEY = ""
UEDITOR_QINIU_SECRET_KEY = ""
UEDITOR_QINIU_BUCKET_NAME = ""
UEDITOR_QINIU_DOMAIN = ""
UEDITOR_UPLOAD_PATH = ""
UEDITOR_UPLOAD_TO_QINIU = False
UEDITOR_UPLOAD_TO_SERVER = False
UEDITOR_UPLOAD_TO_ALIYUN = False
UEDITOR_UPLOAD_TO_TENCENT = False


# 用来判断是否要将文件上传到自己的服务器
try:
    UEDITOR_UPLOAD_TO_SERVER = settings.UEDITOR_UPLOAD_TO_SERVER
    if UEDITOR_UPLOAD_TO_SERVER:
        UEDITOR_UPLOAD_PATH = settings.UEDITOR_UPLOAD_PATH
        if not os.path.exists(UEDITOR_UPLOAD_PATH):
            os.mkdir(UEDITOR_UPLOAD_PATH)
except:
    pass

# 用来判断是否要将文件上传到七牛
try:
    UEDITOR_UPLOAD_TO_QINIU = settings.UEDITOR_UPLOAD_TO_QINIU
except:
    pass

# 用来判断是否要将文件上传到阿里云oss
try:
    UEDITOR_UPLOAD_TO_ALIYUN = meizitu_settings.UEDITOR_UPLOAD_TO_ALIYUN
except:
    pass

# 用来判断是否要健文件上传到腾讯云cos
try:
    UEDITOR_UPLOAD_TO_TENCENT = meizitu_settings.UEDITOR_UPLOAD_TO_TENCENT
except:
    pass


# 如果既没有配置上传到本地，又没有配置上传到七牛，那么就抛出异常
# if not UEDITOR_UPLOAD_PATH and not UEDITOR_UPLOAD_TO_QINIU and not UEDITOR_UPLOAD_TO_ALIYUN and not UEDITOR_UPLOAD_TO_TENCENT:
#     raise RuntimeError("UEditor的UEDITOR_UPLOAD_TO_SERVER或者UEDITOR_UPLOAD_TO_QINIU必须配置一项！")


# 判断是否配置了config.json文件的路径
try:
    UEDITOR_CONFIG_PATH = settings.UEDITOR_CONFIG_PATH
except:
    raise RuntimeError("请配置UEditor的配置文件的路径！")


# 如果配置了七牛的配置信息
if UEDITOR_UPLOAD_TO_QINIU:
    try:
        UEDITOR_QINIU_ACCESS_KEY = settings.UEDITOR_QINIU_ACCESS_KEY
        UEDITOR_QINIU_SECRET_KEY = settings.UEDITOR_QINIU_SECRET_KEY
        UEDITOR_QINIU_BUCKET_NAME = settings.UEDITOR_QINIU_BUCKET_NAME
        UEDITOR_QINIU_DOMAIN = settings.UEDITOR_QINIU_DOMAIN
    except Exception as e:
        option = e.args[0]
        raise RuntimeError('请在app.config中配置%s！'%option)

# 如果配置了阿里云oss则：
if UEDITOR_UPLOAD_TO_ALIYUN:
    try:
        ALIYUN_AccessKey_ID = meizitu_settings.ALIYUN_AccessKey_ID
        ALIYUN_AccessKey_Secret = meizitu_settings.ALIYUN_AccessKey_Secret
        ALIYUN_bucket_name = meizitu_settings.ALIYUN_bucket_name
        ALIYUN_endpoint = meizitu_settings.ALIYUN_endpoint
        ALIYUN_prefix_url = meizitu_settings.ALIYUN_prefix_url
    except Exception as e:
        option = e.args[0]
        raise RuntimeError('请在app.config中配置%s！'%option)


# 如果配置了腾讯云cos则：
if UEDITOR_UPLOAD_TO_ALIYUN:
    try:
        TENCENT_secret_id = meizitu_settings.TENCENT_secret_id
        TENCENT_secret_key = meizitu_settings.TENCENT_secret_key
        TENCENT_bucket_name = meizitu_settings.TENCENT_bucket_name
        TENCENT_region = meizitu_settings.TENCENT_region
        TENCENT_prefix_url = meizitu_settings.TENCENT_prefix_url
    except Exception as e:
        option = e.args[0]
        raise RuntimeError('请在app.config中配置%s！'%option)



@method_decorator([csrf_exempt,require_http_methods(['GET','POST'])],name='dispatch')
class UploadView(View):
    def __init__(self):
        super(UploadView, self).__init__()

    def _random_filename(self,rawfilename):
        """
        随机的文件名，保证文件名称不会冲突
        """
        letters = string.ascii_letters
        random_filename = str(time.time()) + "".join(random.sample(letters, 5))
        filename = hashlib.md5(random_filename.encode('utf-8')).hexdigest()
        subffix = os.path.splitext(rawfilename)[-1]
        return filename + subffix

    def _json_result(self,state='', url='', title='', original=''):
        """
        返回指定格式的json数据的
        """
        result = {
            'state': state,
            'url': url,
            'title': title,
            'original': original
        }
        return JsonResponse(result)

    def _upload_to_qiniu(self,upfile,filename):
        """
        上传文件到七牛
        """
        if not sys.modules.get('qiniu'):
            raise RuntimeError('没有导入qiniu模块！')
        q = qiniu.Auth(UEDITOR_QINIU_ACCESS_KEY, UEDITOR_QINIU_SECRET_KEY)
        token = q.upload_token(UEDITOR_QINIU_BUCKET_NAME)
        buffer = BytesIO()
        for chunk in upfile.chunks():
            buffer.write(chunk)
        buffer.seek(0)
        ret, info = qiniu.put_data(token, filename, buffer.read())
        if info.ok:
            url = parse.urljoin(UEDITOR_QINIU_DOMAIN, ret['key'])
            return 'SUCCESS', url, ret['key'], ret['key']
        else:
            return 'FAIL',None,None,None

    def _upload_to_aliyun(self, upfile, filename):
        '''
        上传到阿里云
        :param upfile:
        :param filename:
        :return:
        '''
        if not sys.modules.get('oss2'):
            raise RuntimeError('没有导入oss2模块！')
        for param in (ALIYUN_AccessKey_ID, ALIYUN_AccessKey_Secret, ALIYUN_bucket_name, ALIYUN_endpoint):
            assert '<' not in param, '请设置参数：' + param
        bucket = oss2.Bucket (oss2.Auth (ALIYUN_AccessKey_ID, ALIYUN_AccessKey_Secret), ALIYUN_endpoint, ALIYUN_bucket_name)
        buffer = BytesIO ()
        for chunk in upfile.chunks ():
            buffer.write (chunk)
        buffer.seek (0)
        ret = bucket.put_object (os.path.join('article', filename).replace('\\', '/'), buffer)
        if ret.status==200:
            # 需要拼接url
            url = os.path.join(ALIYUN_prefix_url,'article', filename).replace('\\', '/')
            print(url)
            return 'SUCCESS', url, None,None
        else:
            return 'FAIL',None,None,None


    def _upload_to_server(self,upfile,filename):
        """
        上传文件到自己的服务器
        """
        # 需要手动创建news_pic文件夹
        if not os.path.exists (settings.MEDIA_ROOT + '/news_pic/'):
            os.makedirs (settings.MEDIA_ROOT + '/news_pic/')
        print(UEDITOR_UPLOAD_PATH)
        print(os.path.join(settings.MEDIA_ROOT, 'news_pic', filename) )
        with open(os.path.join(UEDITOR_UPLOAD_PATH, 'news_pic', filename), 'wb') as fp:
            for chunk in upfile.chunks():
                fp.write(chunk)
        url = reverse("ueditor:send_file", kwargs={"filename": filename})
        return 'SUCCESS', url, filename, filename


    def _action_config(self):
        """
        处理configl类型的响应
        """
        config_path = UEDITOR_CONFIG_PATH
        with open(config_path, 'r', encoding='utf-8') as fp:
            result = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
            return JsonResponse(result)

    def _action_upload(self,request):
        """
        处理文件（图片，视频，普通文件）上传
        """
        upfile = request.FILES.get("upfile")
        filename = self._random_filename(upfile.name)

        qiniu_result = None
        server_result = None
        aliyun_result = None

        if UEDITOR_UPLOAD_TO_QINIU:
            qiniu_result = self._upload_to_qiniu(upfile,filename)

        if UEDITOR_UPLOAD_TO_SERVER:
            server_result = self._upload_to_server(upfile,filename)

        if UEDITOR_UPLOAD_TO_ALIYUN:
            aliyun_result = self._upload_to_aliyun(upfile, filename)

        if qiniu_result and qiniu_result[0] == 'SUCCESS':
            return self._json_result(*qiniu_result)
        elif server_result and server_result[0] == 'SUCCESS':
            return self._json_result(*server_result)
        elif aliyun_result and aliyun_result[0] == 'SUCCESS':
            return self._json_result(*aliyun_result)
        else:
            return self._json_result()


    def _action_scrawl(self,request):
        base64data = request.form.get("upfile")
        img = base64.b64decode(base64data)
        filename = self._random_filename('xx.png')
        with open(os.path.join(UEDITOR_UPLOAD_PATH, filename), 'wb') as fp:
            fp.write(img)
        url = reverse('ueditor:send_file', kwargs={"filename": filename})
        return self._json_result('SUCCESS', url, filename, filename)


    def dispatch(self, request, *args, **kwargs):
        super(UploadView, self).dispatch(request,*args,**kwargs)
        action = request.GET.get('action')
        if action == 'config':
            return self._action_config()
        elif action in ['uploadimage','uploadvideo','uploadfile']:
            return self._action_upload(request)
        elif action == 'uploadscrawl':
            return self._action_scrawl(request)
        else:
            return self._json_result()


# 这个函数就是用来处理已经上传的图片， 在文章里面的显示的函数，就相当于在总URL中后面添加的
# static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)用于显示图片一样，就是展示图片
# 如果你把图片放到阿里云oss中，再把UEDITOR_UPLOAD_TO_SERVER = False，这个函数就不起作用
# 同样本地文件也无法显示在文章详情中
def send_file(request,filename):
    fp = open(os.path.join(UEDITOR_UPLOAD_PATH, 'news_pic',filename),'rb')
    response = FileResponse(fp)
    response['Content-Type'] = "application/octet-stream"
    return response