from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.shortcuts import render, redirect

# Create your views here.
from login.forms import LoginForm, RegisterForm
from login.models import SiteUser, ConfirmString
from login.utils import hash_code, make_confirm_string, send_email
from loginRegister import settings


def index(request):
    if request.session.get('is_login'):
        return render(request, 'login/index.html')
    return redirect('/login/')


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = SiteUser.objects.filter(name=username, password=hash_code(password)).first()
            if user:
                if not user.has_confirmed:
                    message = '该用户还未经过邮件确认！'
                    return render(request, 'login/login.html', locals())
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['username'] = user.name
                return redirect('/index/')
            else:
                message = "用户名或者密码错误"
                return render(request, 'login/login.html', locals())
        else:
            message = "填写的登录信息不合法"
            return render(request, 'login/login.html', locals())
    login_form = LoginForm()
    return render(request, 'login/login.html', locals())


def register(request):
    # 如果用户已经登录，则不能注册跳转到首页。
    if request.session.get('is_login', None):
        return redirect('/index/')
    # 如果是POST请求
    if request.method == 'POST':
        print(request.POST)
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        # 先验证提交的数据是否通过
        if register_form.is_valid():
            # 清洗数据
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')

            # 接下来判断用户名和邮箱是否已经被注册
            same_name_user = SiteUser.objects.filter(name=username)
            print(same_name_user)
            if same_name_user:
                message = '用户名已经存在'
                return render(request, 'login/register.html', locals())
            same_email_user = SiteUser.objects.filter(email=email)
            if same_email_user:
                message = '该邮箱已经被注册了！'
                return render(request, 'login/register.html', locals())
            try:
                # 将注册的信息存储到数据库，跳转到登录界面
                new_user = SiteUser(name=username, password=hash_code(password1), email=email)
                new_user.save()
                # 生成确认码并发送确认邮件
                code = make_confirm_string(new_user)
                print('code:', code)
                send_email(email, code)
                message = '请前往邮箱进行确认！'
            except Exception:
                new_user.delete()
                message = '发送邮件失败！'
                return render(request, 'login/register.html', locals())
            else:
                return redirect('/login/')
    # 如果是GET请求，返回用户注册的html页面。
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    # 如果状态不是登录状态，则无法登出。
    if request.session.get('is_login'):
        request.session.flush()  # 清空session信息
    return redirect('/login/')


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'login/confirm.html', locals())

    create_time = confirm.create_time
    now = datetime.now()
    print(now, create_time, create_time + timedelta(settings.CONFIRM_DAYS))
    if now > create_time + timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
    return render(request, 'login/confirm.html', locals())
