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

**0. 二级菜单以及默认选中设计思路**

**<u>用户登陆 -- 权限初始化 --  通过用户当前的角色跨表获取所有权限及菜单信息（一级菜单与二级菜单） -- 存入session</u>**

```python
permissionQueryset = userObj.roles.filter(permission__isnull=False) \
        .values('permission__id',
                'permission__title',
                'permission__url',
                'permission__name',

                'permission__pid_id',
                'permission__pid__title',
                'permission__pid__url',

                'permission__menu_id',
                'permission__menu__title',
                'permission__menu__icon'
                ).distinct()  # 获取到所有权限(url) 并去重
```

在Menu表中存储的都是一级菜单

在Permission表中存储的都是二级菜单和三级菜单，并且将能作为菜单展示的权限通过外键关联到Menu表中，不能做菜单的权限通过自关联到权限表中的二级菜单权限。

二级菜单通过id归属到一级菜单下，三级菜单通过pid归属到二级菜单下

**在中间件中：循环当前用户的所有权限信息并且手动给request对象赋一个参数：**

```python
request.currentSelectedPermission = item['pid'] or item['id']
```

在这个参数中存储了当前访问权限的pid 或 id，如果存在pid表示当前访问的路由是一个”三级“菜单，即不能作为菜单展示的权限

如果没有pid表示当前访问路由就是一个二级菜单。

**inclusion_tag中读取所有菜单信息进行处理：**

外循环当前用户的所有菜单信息，内循环每个一级菜单下的children（二级菜单信息）；数据结构见下，给一级菜单加上一个默认属性‘hide’让他默认被折叠起来。内循环的时候如果当前访问的路由与权限中的路由一致 且 权限信息中存储的pid或id与二级菜单相同，那么就给这个二级菜单添加一个active属性，让他默认被选中。

假设有这么一个用户拥有这些权限：

```python
# 用户的权限信息
{'id': 1, 'title': '所有部门', 'url': '/stark/crm/department/list/', 'pid': None, 'p_title': None, 'p_url': None}
{'id': 2, 'title': '添加部门', 'url': '/stark/crm/department/add/', 'pid': 1, 'p_title': '所有部门', 'p_url': '/stark/crm/department/list/'}
# 用户的菜单信息
{
    '1': {
        'id': 100
        'title': '客户管理', 
        'icon': 'fa-heart', 
        'children': [
            {'id': 22, 'title': '所有客户', 'url': '/stark/crm/customer/list/'}
        ], 'class': 'hide'
    }, 
    '2': {
        'id': 101
        'title': '员工管理', 
        'icon': 'fa-hourglass', 
        'children': [
            {'id': 42, 'title': '所有员工', 'url': '/stark/crm/staffrecord/list/'}
        ], 'class': 'hide'
    },
    '3': {
        'id': 102
        'title': '分公司管理', 
        'icon': 'fa-retweet', 
        'children': [
            {'id': 1, 'title': '所有部门', 'url': '/stark/crm/department/list/'}, 
            {'id': 10, 'title': '所有项目', 'url': '/stark/crm/project/list/'}, 
            {'id': 14, 'title': '所有城市', 'url': '/stark/crm/city/list/'}, 
            {'id': 18, 'title': '所有分公司', 'url': '/stark/crm/company/list/'}
        ], 'class': 'hide'
    }, 
}
```

此时用户访问的是： “添加部门”这个权限，那么：request.currentSelectedPermission的值为1（pid），在inclusion_tag中循环children（二级菜单）的时候当前路由的id与request.currentSelectedPermission的值相等的只有“所有部门”这个二级菜单，那么此时一级菜单“分公司管理”被展开，“所有部门”默认被选中；

如果访问的是“所有部门”这个权限，那么request对象中存储了的就是当前权限的id(1),在inclusion_tag中循环二级菜单的时候也只有所有部门与之匹配，展示的效果是一样的。



**1. 菜单数据结构模型：**

```python
{
    1:{
        id: 1
        title: '所有客户',
        icon: 'fa-car',
        children: [
            {'id': '1', 'title': '添加客户', 'url': '/userinfo/list/', 'class': 'active'},
            {'id': '2', 'title': '编辑客户', 'url': '/XXXX/list/', 'class': 'active'},
        ], 'class': 'hide'
    },
    2:{
        id: 2,
        title: '所有权限',
        icon: 'fa-permission',
        children: [
            {'id': '1', 'title': '添加权限', 'url': '/permission/list/', 'class': 'active'},
            {'id': '2', 'title': '编辑权限', 'url': '/XXXX/list/', 'class': 'active'},
        ], 'class': 'hide'
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
    ...
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
menu_dict = {
    2: {
        'id': 1, 'title': '菜单一',
    },
    1: {
        'id': 2, 'title': '菜单二',
    }
}

def order_dict():
    dict_list = sorted(menu_dict)
    orderDict = OrderedDict()
    for key in dict_list:
        val = menu_dict[key]
        orderDict[key] = val
	print(orderDict)
    
order_dict()
# OrderedDict(
#     [
#         (1, {'id': 1, 'title': '菜单一'}),
#         (2, {'id': 2, 'title': '菜单二'})
#     ]
# )
```

