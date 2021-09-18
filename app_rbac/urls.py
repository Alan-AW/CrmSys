from django.urls import path, re_path
from app_rbac.views import role  # 角色
from app_rbac.views import user  # 用户
from app_rbac.views import menu  # 菜单

app_name = 'rbac'
urlpatterns = [
    # 角色管理
    path('role/list/', role.RoleList.as_view(), name='role_list'),
    path('role/add/', role.RoleAdd.as_view(), name='role_add'),
    re_path(r'role/edit/(?P<pk>\d+)/$', role.RoleEdit.as_view(), name='role_edit'),
    re_path(r'role/del/(?P<pk>\d+)/$', role.RoleDel.as_view(), name='role_del'),
    # 用户管理
    path('user/list/', user.UserList.as_view(), name='user_list'),
    path('user/add/', user.UserAdd.as_view(), name='user_add'),
    re_path(r'user/edit/(?P<pk>\d+)/$', user.UserEdit.as_view(), name='user_edit'),
    re_path(r'user/del/(?P<pk>\d+)/$', user.UserDel.as_view(), name='user_del'),
    re_path(r'user/reset/(?P<pk>\d+)$', user.ResetPassword.as_view(), name='user_reset'),
    # 一级菜单管理
    path('menu/list/', menu.MenuList.as_view(), name='menu_list'),
    path('menu/add/', menu.MenuAdd.as_view(), name='menu_add'),
    re_path(r'menu/edit/(?P<pk>\d+)/$', menu.MenuEdit.as_view(), name='menu_edit'),
    re_path(r'menu/del/(?P<pk>\d+)/$', menu.MenuDel.as_view(), name='menu_del'),
    # 二级菜单管理
    re_path(r'second/menu/add/(?P<menuId>\d+)/$', menu.SecondMenuAdd.as_view(), name='second_menu_add'),
    re_path(r'second/menu/edit(?P<pk>\d+)/$', menu.second_menu_edit, name='second_menu_edit'),
    re_path(r'second/menu/del(?P<pk>\d+)/$', menu.second_menu_del, name='second_menu_del'),
    # 权限管理
    re_path(r'permission/add/(?P<secondMenuId>\d+)/$', menu.PermissionAdd.as_view(), name='permission_add'),
    re_path(r'permission/edit/(?P<pk>\d+)/$', menu.permission_edit, name='permission_edit'),
    re_path(r'permission/del/(?P<pk>\d+)/$', menu.permission_del, name='permission_del'),
    # 批量操作权限
    path('multi/permissions/', menu.multi_permissions, name='multi_permissions'),
    re_path(r'^multi/permissions/del/(?P<pk>\d+)/$', menu.multi_permissions_del, name='multi_permissions_del'),
    # 权限分配
    path('distribute/permissions/', menu.distribute_permissions, name='distribute_permissions')
]

"""
    反向解析 reverse 在解析带有参数的url时参数传递如下  
    reverse('menu_edit', kwargs={'pk':1})
    reverse('menu_del', args=(1,))
    - 当路由中使用了分组时 /(?P<xxx>\.*)/ 使用kwargs=字典
    - 否则使用args=元组
"""
