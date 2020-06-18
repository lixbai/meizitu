from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from shortuuidfield import ShortUUIDField
from django.db import models

class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError ('请传入邮箱')
        if not username:
            raise ValueError ('请传入用户名')
        if not password:
            raise ValueError ('请传入密码')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        # 创建普通用户
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        # 创建超级用户
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)



# 我们自定义用户的属性，不用系统自带的，系统自带的有很多字段用不到，这里就用比较简单的，因为系统自带的USER也是继承上面两个类，然后自己写的
class User(AbstractBaseUser, PermissionsMixin):
    # 默认不实用默认的自增长主键，用short uuid
    # pip install django-shortuuidfield
    uid = ShortUUIDField(primary_key=True) #主键
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    EMAIL_FIELD = 'email'

    objects = UserManager()