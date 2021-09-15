## **RBAC:Role based user access control**

## 基于权限的动态菜单

**rbac实现流程：1.用户登陆 --> 2.(3)权限初始化(读取当前用户拥有的所有权限，放入session中) --> 3(2).中间件读取权限信息做权限校验**

**<u>在中间件中会读取当前用户请求url，如果是白名单的话会直接放行，进入用户登陆校验，然后做权限初始化。第二次发出请求的时候，穿过中间件的时候仍然会做权限判断，是否登陆、是否有权限访问......</u>**

# 一、inclusion_tag

```python
# 后端代码
# rbac.py
from django.template import Library
register = Library()  # 注册该组件
@register.inclusion_tag('rbac/multiMenu.html')
def multiMenu(request):
    pass

# 前端使用
{% load rbac %}
{% multiMenu request %}
# 一个参数直接写在函数名后面
```

# 二、二级菜单数据构建

**1. 二级菜单数据结构模型：**

```python
{
    1:{
        title: '用户管理',
        icon: 'fa-car',
        children: [
            {'title': '用户列表', 'url': '/userinfo/list/'},
            {'title': 'XXXX列表', 'url': '/XXXX/list/'},
        ]
    },
    2:{
        title: '权限管理',
        icon: 'fa-permission',
        children: [
            {'title': '权限列表', 'url': '/permission/list/'},
            {'title': 'XXXX列表', 'url': '/XXXX/list/'},
        ]
    },
    ......
}
```

**2.数据库支持**

```python
# 新增一个表用来存储一及菜单，
class Menu(models.Model):
    title = models.CharField(verbose_name='一级菜单名称', max_length=32)
    icon = models.Charfield(verbose_name='图标', max_length=32, null=True, blank=True)
    
# 权限表中新增两个字段，将权限归属到菜单中
class Permission(models.Model):
    menu = models.ForeignKey(verbose_name='所属菜单', to='Menu', null=True, blank=True,
                             help_text='null表示不是菜单,这个字段有值才表示二级菜单',
                             on_delete=models.DO_NOTHING)
    pid = models.ForeignKey('self', verbose_name='关联某个权限',
                            help_text='对于非菜单权限需要选择一个可以成为菜单的权限,用户做默认展开和选中的菜单',
                            null=True, blank=True, on_delete=models.DO_NOTHING, related_name='parents')

```

**3.有序字典**

```python
from collections import OrderedDict
menuDict = {'title': 'menu_title', 'url': 'menu_url'}  # 无序字典
keyLIst = sorted(menuDict)  # 对无序字典的key进行排序
orderedDict = OrderedDict()  # 创建了一个空的有序字典
for key in keyLIst:  # 对排序之后的新字典进行循环
    val = menuDict[key]  # 根据有序字典的key去原始无序字典进行取值（取到的都是一级菜单）
    val['class'] = 'hide'  # 给所有的一级菜单默认加了一个hide class属性使其隐藏
    for per in val['children']:  # 再次循环一级菜单中的二级菜单(权限)
        if per['id'] == request.currentSelectedPermission:
            per['class'] = 'active'  # 给自己(二级菜单)加上active class属性
            val['class'] = ''  # 给一级菜单的class hide 属性去掉 让一级菜单保持展开状态
    orderedDict[key] = val

return {'menuDict': orderedDict}
```

