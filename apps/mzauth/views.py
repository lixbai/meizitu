from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm
from django.http import JsonResponse
from utils import restful

@require_POST
def login_view(request):
    # 只要处理前端传回的数据就可以了，就是对数据进行校验
    form = LoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')

        user = authenticate(request, username=email, password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None) #两个星期的有效期
                    return restful.ok()
                else:
                    request.session.set_expiry(0)
                    return restful.ok()
            else:
                return restful.unauth_error(message='您的账号已经被冻结了')
        else:
            return restful.params_error(message='邮箱或者密码错误')
    else:
        errors = form.get_errors()
        return restful.params_error(message=errors)