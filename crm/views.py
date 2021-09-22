from django.shortcuts import render, redirect, reverse
from django.views import View
from django.utils.module_loading import import_string
from django.conf import settings as sys
from crm.models import UserInfo
from app_rbac.service.initPermission import initPermission


class Login(View):
    def __init__(self):
        self.user = import_string(sys.USER_MODEL_CLASS)

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = request.POST.get('user')
        pwd = request.POST.get('password')
        userObj = self.user.objects.filter(username=user, password=pwd).first()
        if not userObj:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
        request.session['user_info'] = {'id': userObj.pk, 'name': userObj.name}
        initPermission(userObj, request)
        return redirect(reverse('welcome'))


class Logout(View):
    def get(self, request):
        request.session.delete()
        return redirect(reverse('login'))


class Welcome(View):
    def get(self, request):
        user_name = request.session.get('user_info')['name']
        return render(request, 'welcome.html', locals())


class NoPermissionHtml(View):
    def get(self, request):
        return render(request, 'no_permission.html')
# class AddCity(View):
#     def get(self, request):
#         return render(request, 'pop.html')
#
#     def post(self, request):
#         name = request.POST.get('city')
#         if name:
#             City.objects.create(title=name)
#             cityObj = City.objects.filter(title=name).first()
#             cityId = cityObj.id
#             cityName = name
#             return render(request, 'pop_close.html', locals())
#         return render(request, 'pop.html')
