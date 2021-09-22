from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponse
from django.utils.module_loading import import_string
from django.conf import settings as sys
from app_rbac.forms.user import UserModelForm, UpdateUserModelForm

"""
    用户管理
"""


class UserList(View):
    def get(self, request):
        obj = import_string(sys.USER_MODEL_CLASS)
        userQuerySet = obj.objects.all()
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
        obj = import_string(sys.USER_MODEL_CLASS)
        userObj = obj.objects.filter(id=pk).first()
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
        obj = import_string(sys.USER_MODEL_CLASS)
        obj.objects.filter(id=pk).delete()
        return redirect(self.cancelUrl)


class ResetPassword(View):
    def get(self, request, pk):
        obj = import_string(sys.USER_MODEL_CLASS)
        userObj = obj.objects.filter(id=pk).first()
        if not userObj:
            user_not_found = '无当前用户！请重新选择！'
            return render(request, 'rbac/resetpwd.html', locals())
        return render(request, 'rbac/resetpwd.html')

    def post(self, request, pk):
        obj = import_string(sys.USER_MODEL_CLASS)
        userObj = obj.objects.filter(id=pk)
        pwd = request.POST.get('password')
        resetpwd = request.POST.get('resetpassword')
        if not pwd or not resetpwd:
            errors = '不能为空！'
            return render(request, 'rbac/resetpwd.html', locals())
        if not userObj or pwd != resetpwd:
            errors = '当前用户不存！或两次输入的密码不一致！'
            return render(request, 'rbac/resetpwd.html', locals())
        userObj.update(password=resetpwd)
        return redirect(reverse('rbac:user_list'))
