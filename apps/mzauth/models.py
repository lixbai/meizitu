from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models

class UserManager(BaseUserManager):
    def _create_user(self,telephone,username,password,**kwargs):
        if not telephone:
            raise ValueError('请传入手机号码！')
        if not username:
            raise ValueError('请传入用户名！')
        if not password:
            raise ValueError('请传入密码！')

        user = self.model(telephone=telephone,username=username,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone,username,password,**kwargs)

    def create_superuser(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone,username,password,**kwargs)



# 我们自定义用户的属性，不用系统自带的，系统自带的有很多字段用不到，这里就用比较简单的，因为系统自带的USER也是继承上面两个类，然后自己写的
class User(AbstractBaseUser, PermissionsMixin):
    # 默认不实用默认的自增长主键，用short uuid
    # pip install django-shortuuidfield
    uid = ShortUUIDField(primary_key=True) #主键
    telephone = models.CharField(max_length=11, unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # 这个是用来验证的，必须填写的。
    USERNAME_FIELD = 'telephone'
    # 这个是当你来创建用户的时候，必填写的几个字段，这里只写了ursername，但是创建用户的时候，还要 捎带上telephone,和password,也就是三个参数。
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username