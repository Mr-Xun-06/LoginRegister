from captcha.fields import CaptchaField
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', required=True, min_length=4, max_length=128)
    password = forms.CharField(label="密码", required=True, min_length=4, max_length=10)
    captcha = CaptchaField(label="验证码")
