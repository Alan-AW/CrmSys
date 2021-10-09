# STARK组件:帮助开发者对数据表快速进行 增删改查+ 的功能组件

#### 一、URL携参数跳转

```python
from django.http import Querydict

def redirect(self):
    # 获取需要跳转的地址
    name = '%s:%s' % (namespace, url_name)  # stark:userinfo_add
    base_url = reverse(name)

    # 获取url中的参数
    param = request.GET.urlencode():  # 地址栏中的所有参数
    if param:
        new_dict = Querydict(mutible=True)  # 可修改参数
        # 携带参数生成跳转地址
        new_dict['_filter'] = param  # 存储GET参数
        add_url = '%s?%s' % (base_url, new_dict.urlencode())  # 目标跳转地址
    else:
        add_url = base_url
```

#### 二、URL携参数跳回

```python
def reverse_list(self):
    # 获取需要跳转的地址
    name = '%s:%s' % (namespace, url_name)  # stark:userinfo_list
    base_url = reverse(name)

    param = request.GET.get('_filter')
    if not param:
        return base_url
    else:
        return '%s?%s' % (base_url, param)
```



