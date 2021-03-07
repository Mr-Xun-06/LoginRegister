from django.shortcuts import render, redirect

# Create your views here.
from login.forms import LoginForm
from login.models import SiteUser


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.method == 'POST':
        # 修改1： 实例化表单对象
        login_form = LoginForm(request.POST)
        # 修改2: 验证表单数据的合法性
        if login_form.is_valid():
            # 修改3：获取表单填写的数据，数据清洗
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
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
                # 修改4: locals()以字典方式返回当前所有的变量
                # eg:{'message':'xxxx', 'login_form':'xxx'}
                return render(request, 'login/login.html', locals())
        else:
            message = "非法的数据信息"
            return render(request, 'login/login.html', locals())
    # 请求方法是GET请求
    login_form = LoginForm()
    return render(request, 'login/login.html', locals())


def register(request):
    pass
    return render(request, 'login/register.html')


def logout(request):
    # 如果状态不是登录状态，则无法登出。
    if request.session.get('is_login'):
        request.session.flush() # 清空session信息
    return redirect('/login/')

