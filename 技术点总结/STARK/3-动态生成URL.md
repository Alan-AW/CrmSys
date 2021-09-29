## **STARK组件:**帮助开发者对数据表快速进行 增删改查+ 的功能组件

## 一、通过Model类获取到app名称和表名称

```python
model_class = models.UserInfo.objects.all()  # model类对象

app_label, model_label = model_class._meta.app_label, model_class._meta.model_label
"""
app_label: model_class._meta.app_label
model_label: model_class._meta.model_label
"""
```

## 二、动态生成URL

```python
if prev:
    # 自定制前缀，并且再次进行路由分发到默认的公共视图函数中生成的增删改查的路由地址
    patterns.append(path('%s/%s/%s/' % (applabel, modelname, prev), (handler.get_urls(), None, None)))
else:
    # 无须自定制前缀，并且再次进行路由分发到默认的公共视图函数中生成的增删改查的路由地址
    patterns.append(path('%s/%s/' % (applabel, modelname), (handler.get_urls(), None, None)))
```

路由中调用动态的URL：

```python
@property
def urls(self):
    return (self.get_url(), self.app_name, self.namespace)

patterns = [
    ...
    path('stark/', site.urls)
]
```





