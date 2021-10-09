# **STARK组件:**帮助开发者对数据表快速进行 增删改查+ 的功能组件

#### URL别名设置思路：

由于URL别名具有唯一性，所以url别名的设置采用的appName_modelName_list（change/add/delete），这样设置会出现一个问题，如果用户在注册的时候传递了一个URL前缀的参数，那么生成的URL别名将没有前缀，假设同一张表需要生成公共路由和私有路由，在私有路由中设置了别名用于区分，那么这个时候生成的路由就无法体现出公共和私有路由的区别，导致别名一致的情况出现。

#### 解决办法：

将用户注册时传递进来的url前缀参数添加到_register列表中实例化处理当前表的视图类中，在这个类中进行判断是否生成含有前缀的URL别名：

```python
# 注册时
class StarkSite():
    def register(self, model_class, handler_class=None, prev=None):
        """
        model_class: 是models中的数据表相关类
        handler_class: 处理请求的视图函数所在的类
        prev: 生成URL的前缀
        """
        # 对于无须自定制视图操作，那么直接使用 StarkHandler 的视图操作
        if not handler_class:
            handler_class = StarkHandler
            self._registry.append({
                'model_class': model_class,
                                
                'handler': handler_class(self, model_class, prev),  # 将注册时指定的URL前缀传递到处理视图的类中用于url别名的设置
                
                'prev': prev}
            )

# 处理表的增删改查视图类
class StarkHandler(object):
    def __init__(self, prev):
        self.prev = prev
    
    def get_url_name(self, param):
        """
        URL别名设置：判断url是否自定制了前缀，用于生成反向解析url别名
        """
        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return '%s_%s_%s_%s' % (app_label, model_name, self.prev, param)
        return '%s_%s_%s' % (app_label, model_name, param)

    @property
    def get_list_url_name(self):
        """
        获取list页面的url别名
        """
        return self.get_url_name('list')

    @property
    def get_add_url_name(self):
        """
        获取添加页面的url别名
        """
        return self.get_url_name('add')

    @property
    def get_edit_url_name(self):
        """
        获取编辑页面的url别名
        """
        return self.get_url_name('edit')

    @property
    def get_delete_url_name(self):
        """
        获取删除页面的url别名
        """
        return self.get_url_name('delete')
    
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
```

