from django.shortcuts import render, redirect, HttpResponse, reverse
from crm import models
from django.utils.safestring import mark_safe
from app_stark.service.StarkModular import site, StarkHandler, get_choices_text, SearchOption
from django.urls import path, re_path
from crm.config.customer import *


class DepartmentConfig(StarkHandler):
    list_display = ['id', 'title', ]
    order_list = ['id', 'title']


class UserConfig(StarkHandler):
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
        if request.method == 'GET':
            user_obj = models.UserInfo.objects.filter(id=user_pk).first()
            if user_obj:
                return render(request, 'stark/detail.html', locals())
            return render(request, 'stark/detail.html', {'not_has_user': True})
        username = request.POST.get('username')
        password = request.POST.get('password')
        if all([username, password]):
            if len(username) >= 3:
                if len(password) > 6:
                    models.UserInfo.objects.filter(id=user_pk).update(username=username, password=password)
                    return redirect(reverse('stark:crm_userinfo_list'))
            else:
                return render(request, 'stark/detail.html', {'defeat': True})
        else:
            return render(request, 'stark/detail.html', {'defeat': True})

    list_display = ['id', display_detail, get_choices_text('性别', 'gender'),
                    'phone', 'email', 'depart', ]
    order_list = ['id', 'name']


class ProjectConfig(StarkHandler):
    list_display = ['id', 'title', ]
    order_list = ['id']


class CityConfig(StarkHandler):
    list_display = ['id', 'name', ]
    order_list = ['id']


# 分公司
class CompanyConfig(StarkHandler):
    list_display = ['id', 'city',
                    'project', 'semester',
                    'price', 'start_date',
                    'end_date', 'manger',
                    'principal', 'memo',
                    ]
    order_list = ['id']


site.register(models.Department, DepartmentConfig)
site.register(models.UserInfo, UserConfig)
site.register(models.Project, ProjectConfig)
site.register(models.City, CityConfig)
site.register(models.Company, CompanyConfig)

# 客户管理
site.register(models.Customer, CustomerConfig)  # 所有客户的管理（最高权限）
site.register(models.Customer, PublicCustomerConfig, 'pub')  # 公户管理
site.register(models.Customer, PrivateCustomerConfig, 'pri')  # 私户管理
site.register(models.ConsultRecord, ConsultRecordConfig)  # 所有客户跟进记录
site.register(models.ConsultRecord, PriConsultRecordConfig, 'pri')  # 私户跟进记录
