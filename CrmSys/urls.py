from django.contrib import admin
from django.urls import path, re_path, include
from crm.views import Index, AddCity
from app_stark.service.v1 import site

urlpatterns = [
    # path('admin/', admin.site.urls),
    # popup 测试代码
    # path('', Index.as_view(), name='index'),
    # path('add/city/', AddCity.as_view(), name='add_city'),

    # stark 组件应用
    path('stark/', site.urls),
    # rbac 组件应用
    path('rbac/', include('app_rbac.urls', namespace='rbac')),
]
