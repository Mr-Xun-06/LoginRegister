from django.contrib import admin

# Register your models here.

from login.models import SiteUser


class SiteUseradmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender']
    list_filter = ['gender', 'create_time']
    search_fields = ['name']


admin.site.register(SiteUser, SiteUseradmin)
