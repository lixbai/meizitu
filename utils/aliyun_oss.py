# -*- coding: utf-8 -*-

import oss2
from meizitu import settings

endpoint = settings.ALIYUN_endpoint # 假设你的Bucket处于杭州区域

auth = oss2.Auth(settings.ALIYUN_AccessKey_ID, settings.ALIYUN_AccessKey_Secret)
bucket = oss2.Bucket(auth, endpoint, settings.ALIYUN_bucket_name)

a_prefix_url = settings.ALIYUN_prefix_url