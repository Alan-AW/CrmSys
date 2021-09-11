from django.template import Library
from CrmSys import settings as sys
from django.urls import reverse
from django.http import QueryDict
import re
from collections import OrderedDict
from app_rbac.service import urls

register = Library()  # 注册该组件


###################### 一级菜单和二级菜单只能选一个 #############################

# 一级菜单
# @register.inclusion_tag('rbac/staticMenu.html')
# def staticMenu(request):
#     menuList = request.session[SYS.MENU_SESSION_KEY]
#     return {
#         'menuList': menuList
#     }

# 二级菜单
@register.inclusion_tag('rbac/multiMenu.html')
def multiMenu(request):
    menuDict = request.session[sys.MENU_SESSION_KEY]
    keyLIst = sorted(menuDict)  # 对字典的key进行排序
    orderedDict = OrderedDict()  # 创建了一个空的有序字典
    for key in keyLIst:
        val = menuDict[key]
        val['class'] = 'hide'  # 默认加了一个hide属性使其隐藏
        for per in val['children']:
            if per['id'] == request.currentSelectedPermission:
                per['class'] = 'active'
                val['class'] = ''
        orderedDict[key] = val

    return {'menuDict': orderedDict}


# 路径导航
@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'recordList': request.breadcrumb}


# 权限粒度控制到按钮
@register.filter
def hasPermission(request, name):
    if name in request.session[sys.PERMISSION_SESSION_KEY]:
        return True


'''
模版中的使用：
加上判断语句
filter “函数可以作为模版的条件进行判断”
    {% if request|hasPermission:'payment_edit' %}
        <xxx>{{ xxx }}</xxx>
    {% endif %}
    
    {% if request|hasPermission:'payment_del' or request|hasPermission:'payment_edit' %}
        <xxx>{{ xxx }}</xxx>
    {% endif %}
'''


# 菜单管理url记忆功能
@register.simple_tag
def memoryUrl(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的url，替代模版中的url(url携带参数)
    :param request:
    :param name:
    :return:
    """
    return urls.memoryUrl(request, name, *args, **kwargs)
