## **STARK组件:**帮助开发者对数据表快速进行 增删改查+ 的功能组件

## 一、Django系统启动时

#### 1.在stark组件(APP)中的app.py对应的视图类中定义一个ready方法，项目启动的时候会去执行该方法

#### 2.执行ready方法时，ready方法自动导入并且执行了一个“stark.py”文件

#### 3.stark.py文件：这个文件是在业务APP中手动创建的。在该文件中需要导入stark组件(APP)提供 的一个site实例化对象

#### 4.使用stark组件(APP)：在stark.py 中写上以下内容，即可实现对一个表的增删改查+的功能

```python
from app_stark.servers.StarkSite import site
from 业务APP import models

site.register(models.XXX, None, None)
```

## 二、Django读取URL时

#### **1.在settings配置文件中定义了项目的根路由地址，当项目启动的时候会去根路由地址中读取路由，对于需要使用stark组件的路由地址，定义的是一个方法：**

根路由：urls.py中

```python
from from app_stark.servers.StarkSite import site

patterns = [
    ...
    path('stark/', site.urls),
]
```

#### **2. site实例化的对象：**

```python
class StarkSite(object):
    def __init__(self):
        self._registry = list()
        self.app_name = 'app_stark'
        self.namespace = 'stark'

    def register(self, model_class, handler_class=None, prev=None):
        # 对于无须自定制视图操作，那么直接使用 StarkHandler 的视图操作
        if not handler_class:
            handler_class = StarkHandler
        self._registry.append({
            'model_class': model_class,
            'handler': handler_class(self, model_class, prev),
            'prev': prev}
        )

    def get_url(self):
        patterns = list()
        for item in self._registry:
            model_class = item['model_class']
            handler = item['handler']
            prev = item['prev']
            applabel, modelname = model_class._meta.app_label, model_class._meta.model_name
            # 再次进行路由分发，支持自定制生成不同的URL
            if prev:
                # 自定制前缀
                patterns.append(path('%s/%s/%s/' % (applabel, modelname, prev), (handler.get_urls(), None, None)))
            else:
                # 无须自定制前缀
                patterns.append(path('%s/%s/' % (applabel, modelname), (handler.get_urls(), None, None)))
        return patterns

    @property
    def urls(self):
        return (self.get_url(), self.app_name, self.namespace)
```

**3. site实例化的对象分为两部分：**

第一部分：在 Django 项目启动的时候调用了register方法，该方法接收了一系列的参数并且进行保存到_registry这个列表中；参数分别有：需要操作的数据库表的类、用于操作这个表的增删改查功能的视图类、路由前缀

第二部分：在Django项目读取路由的时候，读取到了site.urls方法，这个时候会再次进入site实例化的对象(这个StarkSite类中)；该方法返回了一个元祖，第一个参数调用了get_url()方法；

​					而在get_url()方法中再次去读取到了Django项目启动时往 _registry 列表中添加的参数，进而动态的生成了一个path路由列表，并且这个路由再次进行了路由分发，用于自定义动态生成更多的路由

第三部分：实际上用户访问请求的路由是由第二部分路由分发到默认的视图函数中的路由，且使用了stark组件内部提取出来公共的视图函数去操作表的增删改查功能

```python
class StarkHandler(object):
    def __init__():
        pass
    
    def get_urls(self):
        """
            默认生成4组增删改查功能路由。如需自定制功能路由可在APP下的stark中重写该方法实现自动定制
        """
        patterns = [
            path('list/', self.wrapper(self.changelist_view), name=self.get_list_url_name),
            path('add/', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path('edit/(?P<pk>\d+)/$', self.wrapper(self.edit_view), name=self.get_edit_url_name),
            re_path('delete/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]
        # 将用户自定制的URL路由(extend)扩展到全局路由中，而不是将用户自定制的路由列表(append)追加进来
        patterns.extend(self.extra_urls())  # 此处不会直接调用本方法中的extra_urls，self代指的是APP中自定制的视图类，
        return patterns

    def extra_urls(self):
        return []
```

