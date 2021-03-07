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
            user = SiteUser.objects.filter(name=username,password=password).first()
            if user:
                # ------------核心修改的内容开始
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['username'] = user.name
                # --------------核心修改的内容结束
                return redirect('/index/')
            else:
                message = "用户名或者密码错误"
                return render(request, 'login/login.html',{'message':message})
        else:
            message = "非法的数据信息"
            return render(request, 'login/login.html', {'message': message})
    return render(request, 'login/login.html')


def register(request):
    pass
    return render(request, 'login/register.html')


def logout(request):
    # 如果状态不是登录状态，则无法登出。
    if request.session.get('is_login'):
        request.session.flush() # 清空session信息
    return redirect('/login/')

