from django.contrib import admin  # django后台管理
from django.urls import path, re_path, include  # 路由，正则路由， 路由分发
from crm.views import Index, AddCity
from app_stark.service.v1 import site

urlpatterns = [
    path('admin/', admin.site.urls),
    # popup 测试代码
    path('', Index.as_view(), name='index'),
    path('add/city/', AddCity.as_view(), name='add_city'),

    # stark 组件应用
    path('stark/', site.urls),
]
