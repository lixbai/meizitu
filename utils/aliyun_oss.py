# -*- coding: utf-8 -*-

import oss2

endpoint = 'oss-cn-beijing.aliyuncs.com' # 假设你的Bucket处于杭州区域

auth = oss2.Auth('', '')
bucket = oss2.Bucket(auth, endpoint, '')

a_prefix_url = 'https://lixbai.oss-cn-beijing.aliyuncs.com/'