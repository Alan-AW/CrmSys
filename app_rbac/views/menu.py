from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.utils.module_loading import import_string
from django.forms import formset_factory
from django.conf import settings as sys
from collections import OrderedDict

from app_rbac import models
from app_rbac.forms.menu import MenuModelForm, \
    SecondMenuModelForm, PermissionModelForm, \
    MultiAddPermissionForm, \
    MultiEditPermissionForm
from app_rbac.models import *
from app_rbac.service.urls import memoryReverse
from app_rbac.service.routes import AutoFindUrl

"""
一级菜单管理
"""


class MenuList(View):
    """
    所有菜单
    """

    def get(self, request):
        menu = Menu.objects.all()
        menuId = request.GET.get('mid')  # 用户选择的一级菜单
        secondMenuId = request.GET.get('sid')  # 用户选择的二级菜单
        # get方法拿到的mid是字符串类型，前端页面做判断的时候从数据库中取出的id是整型

        # 在没有选中一级菜单的情况下是否展示新增按钮：
        menu_exists = Menu.objects.filter(id=menuId).exists()
        if not menu_exists:
            menuId = None

        if menuId:
            secondMenus = Permission.objects.filter(menu_id=menuId)  # 根据选择的一级菜单获取倒二级菜单
        else:
            secondMenus = []

        # 在没有选中二级菜单的情况下是否展示新增按钮：
        second_menu_exists = Permission.objects.filter(id=secondMenuId).exists()
        if not second_menu_exists:
            secondMenuId = None
        if secondMenuId:
            permissions = Permission.objects.filter(pid=secondMenuId)  # 根据选择的二级菜单查询到对应的所有权限
        else:
            permissions = []

        return render(request, 'rbac/menu_list.html', locals())

    def post(self, request):
        pass


class MenuAdd(View):
    """
    添加一级菜单
    """

    def get(self, request):
        form = MenuModelForm
        return render(request, 'rbac/change.html', locals())

    def post(self, request):
        form = MenuModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            url = memoryReverse(request, 'rbac:menu_list')
            return redirect(url)
        else:
            return render(request, 'rbac/change.html', locals())


class MenuEdit(View):
    """
    菜单修改
    """

    def get(self, request, pk):
        menuObj = Menu.objects.filter(id=pk).first()
        if not menuObj:
            return HttpResponse('禁止操作!')  # 角色不存在
        form = MenuModelForm(instance=menuObj)
        return render(request, 'rbac/change.html', locals())

    def post(self, request, pk):
        menuObj = Menu.objects.filter(id=pk).first()
        form = MenuModelForm(instance=menuObj, data=request.POST)
        if form.is_valid():
            form.save()
            url = memoryReverse(request, 'rbac:menu_list')
            return redirect(url)


class MenuDel(View):
    """
    菜单删除
    """

    def get(self, request, pk):
        url = memoryReverse(request, 'rbac:menu_list')
        return render(request, 'rbac/delete.html', {'cancelUrl': url})

    def post(self, request, pk):
        Menu.objects.filter(id=pk).delete()  # 删除
        # 拼接出原搜索条件url，进行跳转
        url = memoryReverse(request, 'rbac:menu_list')
        return redirect(url)


"""
二级菜单管理
"""


class SecondMenuAdd(View):

    def get(self, request, menuId):
        """
        二级菜单的添加
        :param request:
        :param menuId: 默认的一级菜单ID(用于设置默认值)
        :return:
        """
        menuObj = Menu.objects.filter(id=menuId).first()
        form = SecondMenuModelForm(initial={'menu': menuObj})
        return render(request, 'rbac/change.html', locals())

    def post(self, request, menuId):
        form = SecondMenuModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            url = memoryReverse(request, 'rbac:menu_list')
            return redirect(url)
        else:
            return render(request, 'rbac/change.html', locals())


def second_menu_edit(request, pk):
    permissionObj = Permission.objects.filter(id=pk).first()
    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permissionObj)
        return render(request, 'rbac/change.html', locals())

    form = SecondMenuModelForm(data=request.POST, instance=permissionObj)
    if form.is_valid():
        form.save()
        return redirect(memoryReverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', locals())


def second_menu_del(request, pk):
    url = memoryReverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancelUrl': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


"""
权限管理
"""


class PermissionAdd(View):
    """
    添加权限
    """

    def get(self, request, secondMenuId):
        # menuObj = Menu.objects.filter(id=menuId).first()
        form = PermissionModelForm()
        return render(request, 'rbac/change.html', locals())

    def post(self, request, secondMenuId):
        form = PermissionModelForm(data=request.POST)
        if form.is_valid():
            secondMenuObj = Permission.objects.filter(id=secondMenuId).first()
            if not secondMenuObj:
                return HttpResponse('当前二级菜单不存在，请重新选择二级菜单！')
            # form.instance中：包含了用户提交的所有值
            form.instance.pid = secondMenuObj
            """
             ↑ 这句话相当于执行了三次操作
            - instance = Permission(title='用户输入值', url='用户输入', name='用户输入')
            - instance.pid = secondMenuObj
            - instance.save()
            form.save()
            其实就是保存数据倒数据库中， 表单收集倒的用户输入的数据已经被实例化为了一个对象 ————> instance
            """
            form.save()
            url = memoryReverse(request, 'rbac:menu_list')
            return redirect(url)
        else:
            return render(request, 'rbac/change.html', locals())


def permission_edit(request, pk):
    """
    编辑权限
    :param request:
    :param pk: 当前编辑的权限的pk
    :return:
    """
    permissionObj = Permission.objects.filter(id=pk).first()
    if request.method == 'GET':
        form = PermissionModelForm(instance=permissionObj)
        return render(request, 'rbac/change.html', locals())
    form = PermissionModelForm(data=request.POST, instance=permissionObj)
    if form.is_valid():
        form.save()
        return redirect(memoryReverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', locals())


class PermissionEdit(View):
    """
    类方法实现编辑当前权限路由
    """

    def get(self, request, pk):
        permissionObj = models.Permission.objects.filter(id=pk).first()
        form = PermissionModelForm(instance=permissionObj)
        return render(request, 'rbac/change.html', locals())

    def post(self, request, pk):
        permissionObj = models.Permission.objects.filter(id=pk).first()
        form = PermissionModelForm(instance=permissionObj)
        if form.is_valid():
            form.save()
            return redirect(memoryReverse(request, 'rbac:menu_list'))


def permission_del(request, pk):
    """
    删除权限路由
    :param request:
    :param pk: 当前删除的权限pk
    :return:
    """
    url = memoryReverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancelUrl': url})
    Permission.objects.filter(id=pk).delete()
    return redirect(url)


class PermissionDel(View):
    """
    类方法删除当前权限信息
    """

    def get(self, request):
        url = memoryReverse(request, 'rbac:menu_list')
        return render(request, 'rbac/delete.html', {'cancelUrl': url})

    def post(self, request, pk):
        url = memoryReverse(request, 'rbac:menu_list')
        models.Permission.objects.filter(id=pk).delete()
        return redirect(url)


"""
    权限的批量操作
"""


def multi_permissions(request):
    post_type = request.GET.get('type')
    generate_formset_class = formset_factory(MultiAddPermissionForm, extra=0)  # 批量添加的类
    generate_formset = None
    update_formset = None
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)  # 批量更新的类
    if request.method == 'POST' and post_type == 'generate':
        # 批量添加
        formset = generate_formset_class(data=request.POST)
        if formset.is_valid():
            object_list = []  # 要添加的数据
            post_row_list = formset.cleaned_data
            has_error = False
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_obj = Permission(**row_dict)
                    new_obj.validate_unique()
                    object_list.append(new_obj)  # 检测通过直接append到批量添加的数据中然后批量添加
                except Exception as e:
                    has_error = True
                    formset.errors[i].update(e)
                    generate_formset = formset
            if not has_error:
                Permission.objects.bulk_create(object_list, batch_size=100)  # 没有错误信息的时候直接批量添加操作
        else:
            generate_formset = formset

    if request.method == 'POST' and post_type == 'update':
        # 批量更新
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')
                try:
                    row_obj = Permission.objects.filter(id=permission_id).first()
                    for k, v in row_dict.items():
                        setattr(row_obj, k, v)
                    row_obj.validate_unique()
                    row_obj.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset
        else:
            update_formset = formset

    # 1.获取项目中的url
    auto_find_url = AutoFindUrl()
    all_url = auto_find_url.get_all_url_dict()
    router_name_set = set(all_url.keys())

    # 2.获取数据库中的url
    permission = Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id')
    permission_dict = OrderedDict()
    permission_name_set = set()
    for row in permission:
        permission_dict[row['name']] = row
        # {
        # 'rbac:role_list': {'id':1, 'title': '角色列表', 'name': 'role_list', 'url': '/rbac/role/list/'........}
        # 'rbac:role_add': {'id':1, 'title': '角色添加', 'name': 'role_add', 'url': '/rbac/role/add/'........}
        # }
        permission_name_set.add(row['name'])  # 添加进字典方法一
    # permission_name_set = set(permission_dict.keys())  # 添加进字典方法二

    for name, value in permission_dict.items():
        router_row_dict = all_url.get(name)
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = '陆游哦与数据库中不一致，请检查'

    # 3.应该添加、删除、或者修改的权限有哪些
    # 3.1 计算出应该增加的 name
    if not generate_formset:
        generate_name_list = router_name_set - permission_name_set
        generate_formset = generate_formset_class(
            initial=[row_dict for name, row_dict in all_url.items() if name in generate_name_list])
    # 3.2 计算出应该删除的url
    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]

    # 3.3 计算出更新的url
    if not update_formset:
        update_name_list = permission_name_set & router_name_set
        update_formset = update_formset_class(
            initial=[row_dict for name, row_dict in all_url.items() if name in update_name_list]
        )  # generate_formset --> 当项目中的一条url与数据库中的url完全相同的时候哦可以用update_name_list中的数据，
    # 但是如果同一条url在数据库中的数据与项目中的数据不一致的情况下应该让用户主动去选择而不是默认以数据库中的为准
    # 所以在这些操作之前进行了一个判断 router_row_dict 第292行
    return render(request, 'rbac/multi_permission.html', {
        'generate_formset': generate_formset,
        'delete_row_list': delete_row_list,
        'update_formset': update_formset
    })


def multi_permissions_del(request, pk):
    url = memoryReverse(request, 'rbac:multi_permissions')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancelUrl': url})
    Permission.objects.filter(id=pk).delete()
    return redirect(url)


"""
权限分配
"""


def distribute_permissions(request):
    """
    权限的分配
    """
    # 首先获取到业务逻辑中的用户表
    user_class = import_string(sys.USER_MODEL_CLASS)

    # 获取到当前选择的用户id
    user_id = request.GET.get('uid')
    user_obj = user_class.objects.filter(id=user_id).first()
    if not user_obj:
        user_id = None
    # 获取当前选择的角色id
    r_id = request.GET.get('r_id')
    role_obj = Role.objects.filter(id=r_id).first()
    if not role_obj:
        r_id = None

    # POST提交的数据进行保存
    if request.method == 'POST':
        style_type = request.POST.get('type')
        if style_type == 'role':
            roles_id_list = request.POST.getlist('roles')
            # 把用户和角色的关系添加到关系表中manytomany的关系操作
            if not user_obj:
                return HttpResponse('请不要违规操作！必须先选择用户再做角色的分配')
            user_obj.roles.set(roles_id_list)
        elif style_type == 'permission':
            permission_id_list = request.POST.getlist('permissions')
            # 把权限和角色的关系添加到关系表中manytomany的关系操作
            if not role_obj:
                return HttpResponse('请不要违规操作！必须先选择角色再做权限的分配')
            role_obj.permission.set(permission_id_list)

    # 根据当前用户查询到拥有的所有角色的id，前端进行判断默认选中当前用户的所有角色
    if user_id:  # 验证用户是否存在
        user_has_roles = user_obj.roles.all()
    else:
        user_has_roles = []
    user_has_roles_dict = {item.id: None for item in user_has_roles}  # 字典生成
    # 权限默认选中的展示
    # 如果选择了角色，那么有限显示该角色所拥有的权限
    if role_obj:  # 选择了角色
        user_has_permissions = role_obj.permission.all()
        user_has_permissions_dict = {item.id: None for item in user_has_permissions}
    elif user_obj:  # 未选中角色但是选中了用户
        user_has_permissions = user_obj.roles.filter(permission__id__isnull=False) \
            .values('id', 'permission').distinct()
        user_has_permissions_dict = {item['permission']: None for item in user_has_permissions}
    else:
        user_has_permissions_dict = {}
        # 如果没有选择角色，那么就显示该用户的所有的权限

    # 获取所有的用户
    all_user_list = user_class.objects.all()
    # 获取所有的角色
    all_role_list = Role.objects.all()
    # 构造权限的数据结构
    menu_permissions_list = []
    # 1. 获取所有的一级菜单
    all_menu_list = Menu.objects.values('id', 'title')
    all_menu_dict = {}
    for item in all_menu_list:
        item['children'] = []
        all_menu_dict[item['id']] = item
    # 2. 获取所有的二级菜单  菜单不为空，则表示为二级菜单
    all_second_menu_list = Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')
    all_second_menu_dict = {}
    for row in all_second_menu_list:
        row['children'] = []
        all_second_menu_dict[row['id']] = row
        menu_id = row['menu_id']
        all_menu_dict[menu_id]['children'].append(row)
    # 3. 获取所有的三级菜单（不能做菜单的权限
    all_permission_list = Permission.objects.filter(menu__isnull=True).values('id', 'title', 'pid_id')  # 归属到二级菜单
    for row in all_permission_list:
        pid = row['pid_id']
        if not pid:  # 数据不合法，不做处理
            continue
        all_second_menu_dict[pid]['children'].append(row)

    """
    [
        {
        id:1,
         'title': '业务管理',
         children: [{
            id: 1,
            'title': '权限信息',
            children: [{
                xxxxxxxx
            }]
         }]
        },
    ]
    """

    return render(request, 'rbac/distribute_permissions.html', locals())
