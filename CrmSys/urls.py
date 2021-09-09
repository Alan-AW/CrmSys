from django.contrib import admin
from django.urls import path, re_path, include
from crm.views import Index, AddCity
from app_stark.service.StarkModular import site
from crm.views import Login, Logout

urlpatterns = [
    # path('admin/', admin.site.urls),
    # popup 测试代码
    # path('', Index.as_view(), name='index'),
    # path('add/city/', AddCity.as_view(), name='add_city'),

    # 用户登陆&退出
    path('', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    # stark 组件应用
    path('stark/', site.urls),
    # rbac 组件应用
    path('rbac/', include('app_rbac.urls', namespace='rbac')),

]
