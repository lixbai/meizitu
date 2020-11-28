from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm
from utils import restful
from django.views.generic import View
from django.shortcuts import render, redirect


class LoginView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        # 只要处理前端传回的数据就可以了，就是对数据进行校验
        form = LoginForm(request.POST)
        if form.is_valid():
            #获取form里面的数据
            telephone = form.cleaned_data.get('telephone')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')

            #调用authenticate函数验证传进来的手机号密码，是不是正确的
            user = authenticate(request, telephone=telephone, password=password)
            #如果正确得到user
            if user:
                if user.is_active:
                    login(request,user)
                    if remember:
                        request.session.set_expiry(None)#两个星期的有效期
                        return redirect('cms:cms_index') #登陆成功之后重定向到cms后台首页,这里的登陆比较简单，没有用js代码所以有所区别。
                    else:
                        request.session.set_expiry(0)
                        return redirect('cms:cms_index') #登陆成功之后重定向到cms后台首页
                else:
                    return restful.unauth_error(message='您的账号有问题，请联系管理员')
            else:
                return restful.params_error(message='账号或者密码填错了，请检查！')
        else:
            return restful.params_error(message=form.errors)