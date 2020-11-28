from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError

import sys
import logging


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 设置用户属性, 包括secret_id, secret_key, region
# appid已在配置中移除,请在参数Bucket中带上appid。Bucket由bucketname-appid组成
secret_id = 'AKIDWnqezIP9xWqtgMGELCPN4Wr9D0mO9yqh'     # 替换为用户的secret_id
secret_key = 'rSeBftrFPL2SqEhvCpvlKdwqZlqniPwF'     # 替换为用户的secret_key
region = 'ap-nanjing'    # 替换为用户的region
token = None               # 使用临时密钥需要传入Token，默认为空,可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme='http')  # 获取配置对象
client = CosS3Client(config)

t_prefix_url = 'https://li-1302251434.cos.ap-nanjing.myqcloud.com/'
