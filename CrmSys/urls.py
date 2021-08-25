from django.contrib import admin  # django后台管理
from django.urls import path, re_path, include  # 路由，正则路由， 路由分发

urlpatterns = [
    path('admin/', admin.site.urls),
]
