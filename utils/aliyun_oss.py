# -*- coding: utf-8 -*-

import oss2

endpoint = 'oss-cn-beijing.aliyuncs.com' # 假设你的Bucket处于杭州区域

auth = oss2.Auth('LTAI4FyHYJUPJ3CwZc4kDJBd', 'XbmsSINL3o9bbum3H6AQkyBytledho')
bucket = oss2.Bucket(auth, endpoint, 'lixbai')

a_prefix_url = 'https://lixbai.oss-cn-beijing.aliyuncs.com/'