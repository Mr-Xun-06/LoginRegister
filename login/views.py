from django.shortcuts import render, redirect

# Create your views here.
from login.models import SiteUser


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        # print(username, password)
        if username and password:
            user = SiteUser.objects.filter(name=username,
                                           password=password).first()
            if user:
                return redirect('/index/')
            else:
                message = "用户名或者密码错误"
                return render(request, 'login/login.html',
                              {'message': message})
        else:
            message = "非法的数据信息"
            return render(request, 'login/login.html', {'message': message})
    return render(request, 'login/login.html')


def register(request):
    pass
    return render(request, 'login/register.html')


def logout(request):
    pass
    # redirect: 重定向(跳转)
    return redirect('/login/')
