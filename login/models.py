from django.db import models


# Create your models here.

# appname_siteuser
class SiteUser(models.Model):
    """用户的数据库模型，注册/登陆需要"""
    gender_choice = (
        (0, "未知"),
        (1, "男"),
        (2, "女"),
    )
    name = models.CharField(max_length=128, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=256, verbose_name="密码")
    email = models.EmailField(unique=True, verbose_name="电子邮件")
    gender = models.IntegerField(choices=gender_choice, default=0, verbose_name="性别")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="最后一次修改时间")
    last_login_time = models.DateTimeField(null=True, blank=True, verbose_name="最后一次登陆时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "网站用户管理"
        verbose_name_plural = verbose_name
