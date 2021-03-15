from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError

from meizitu import settings

import sys
import logging


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 设置用户属性, 包括secret_id, secret_key, region
# appid已在配置中移除,请在参数Bucket中带上appid。Bucket由bucketname-appid组成
secret_id = settings.TENCENT_secret_id     # 替换为用户的secret_id
secret_key = settings.TENCENT_secret_key    # 替换为用户的secret_key
region = settings.TENCENT_region    # 替换为用户的region
token = None               # 使用临时密钥需要传入Token，默认为空,可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme='http')  # 获取配置对象
client = CosS3Client(config)

t_prefix_url = settings.TENCENT_prefix_url
