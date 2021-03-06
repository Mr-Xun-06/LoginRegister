# Generated by Django 3.1.7 on 2021-03-06 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=256, verbose_name='密码')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='电子邮件')),
                ('gender', models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0, verbose_name='性别')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='最后一次修改时间')),
                ('last_login_time', models.DateTimeField(blank=True, null=True, verbose_name='最后一次登陆时间')),
            ],
        ),
    ]