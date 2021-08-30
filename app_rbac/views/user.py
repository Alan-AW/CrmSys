from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponse
from app_rbac.models import UserInfo
from app_rbac.forms.user import UserModelForm, UpdateUserModelForm

"""
    用户管理
"""


class UserList(View):
    def get(self, request):
        userQuerySet = UserInfo.objects.all()
        return render(request, 'rbac/user_list.html', locals())


class UserAdd(View):
    def get(self, request):
        form = UserModelForm()
        return render(request, 'rbac/change.html', locals())

    def post(self, request):
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:user_list'))
        else:
            return render(request, 'rbac/change.html', locals())


class UserEdit(View):
    def get(self, request, pk):
        userObj = UserInfo.objects.filter(id=pk).first()
        if not userObj:
            return HttpResponse('该用户不存在!')
        form = UpdateUserModelForm(instance=userObj)
        return render(request, 'rbac/change.html', locals())

    def post(self, request, pk):
        form = UpdateUserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:user_list'))
        else:
            return render(request, 'rbac/change.html', locals())


class UserDel(View):
    def __init__(self):
        self.cancelUrl = reverse('rbac:user_list')

    def get(self, request, pk):
        return render(request, 'rbac/delete.html', {'cancelUrl': self.cancelUrl})

    def post(self, request, pk):
        UserInfo.objects.filter(id=pk).delete()
        return redirect(self.cancelUrl)

