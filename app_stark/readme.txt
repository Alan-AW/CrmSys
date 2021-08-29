stark组件使用文档

1. 拷贝app_stark到任何系统
2. 目标项目中注册app_stark： 'app_stark.apps.AppStarkConfig',
3. 目标app的根目录中创建stark.py文件
4. 配置路由信息：
    from app_stark.service.v1 import site
    path('stark/', site.urls),
