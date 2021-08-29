from django.shortcuts import render, redirect, HttpResponse, reverse
from crm import models
from django.utils.safestring import mark_safe
from app_stark.service.v1 import site, StarkHandler, get_choices_text
from django.urls import path, re_path


class DepartmentHandler(StarkHandler):
    list_display = ['id', 'title', StarkHandler.display_edit, StarkHandler.display_del]
    order_list = ['id', 'title']


class UserHandler(StarkHandler):
    def display_detail(self, obj, is_header=None):
        # 详情页面超链接显示信息以及url反向生成
        if is_header:
            return '详细信息'
        url = reverse('stark:crm_userinfo_detail', kwargs={'user_pk': obj.pk})
        return mark_safe('<a href="%s">%s</a>' % (url, obj.name))

    def extra_urls(self):
        # 增加一条用户详情页面
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        urlpatterns = [
            re_path('(?P<user_pk>\d+)/detail/$', self.wrapper(self.detail_view), name='%s_%s_detail' % info)
        ]
        return urlpatterns

    def detail_view(self, request, user_pk):
        # 用户详情页面渲染
        return HttpResponse('查看详细页面')

    list_display = ['id', display_detail, get_choices_text('性别', 'gender'),
                    'phone', 'email', 'depart',
                    StarkHandler.display_edit,
                    StarkHandler.display_del]
    order_list = ['id', 'name']


class ProjectHandler(StarkHandler):
    list_display = ['id', 'title', StarkHandler.display_edit, StarkHandler.display_del]
    order_list = ['id']


class CityHandler(StarkHandler):
    list_display = ['id', 'name', StarkHandler.display_edit, StarkHandler.display_del]
    order_list = ['id']


class CompanyHandler(StarkHandler):
    list_display = ['id', 'city',
                    'project', 'semester',
                    'price', 'start_date',
                    'end_date', 'manger',
                    'principal', 'memo',
                    StarkHandler.display_edit, StarkHandler.display_del]
    order_list = ['id']


site.register(models.Department, DepartmentHandler)
site.register(models.UserInfo, UserHandler)
site.register(models.Project, ProjectHandler)
site.register(models.City, CityHandler)
site.register(models.Company, CompanyHandler)
