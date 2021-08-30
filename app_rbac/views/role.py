from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.views import View
from app_rbac.forms.role import RoleModelForm
from app_rbac.models import *


"""
    角色管理
"""
class RoleList(View):
    """
    角色列表
    """

    def get(self, request):
        roleQuerySet = Role.objects.all()
        return render(request, 'rbac/role_list.html', locals())


class RoleAdd(View):
    """
    添加角色
    """

    def get(self, request):
        form = RoleModelForm
        return render(request, 'rbac/change.html', locals())

    def post(self, request):
        form = RoleModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:role_list'))
        else:
            return render(request, 'rbac/change.html', locals())


class RoleEdit(View):
    """
    角色编辑
    """

    def get(self, request, pk):
        roleObj = Role.objects.filter(id=pk).first()
        if not roleObj:
            return HttpResponse('禁止操作!')  # 角色不存在
        form = RoleModelForm(instance=roleObj)
        return render(request, 'rbac/change.html', locals())

    def post(self, request, pk):
        roleObj = Role.objects.filter(id=pk).first()
        form = RoleModelForm(instance=roleObj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:role_list'))


class RoleDel(View):
    """
    删除角色
    """

    def __init__(self):
        # 为了所有的删除确认页面都通用，这里给一个参数 cancelUrl作为取消按钮的url跳转地址
        self.cancelUrl = reverse('rbac:role_list')

    def get(self, request, pk):
        return render(request, 'rbac/delete.html', {'cancelUrl': self.cancelUrl})

    def post(self, request, pk):
        Role.objects.filter(id=pk).delete()  # 删除
        return redirect(self.cancelUrl)















