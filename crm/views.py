from django.shortcuts import render, redirect, reverse
from django.views import View
from crm.models import *
from app_rbac.service.initPermission import initPermission


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = request.POST.get('user')
        pwd = request.POST.get('password')
        userObj = UserInfo.objects.filter(username=user, password=pwd).first()
        if not userObj:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
        initPermission(userObj, request)
        return redirect(reverse('rbac:menu_list'))


class Logout(View):
    def get(self, request):
        request.session.delete()
        return redirect(reverse('login'))


class Index(View):
    def get(self, request):
        all_city = City.objects.all()
        return render(request, 'index.html', locals())


class AddCity(View):
    def get(self, request):
        return render(request, 'pop.html')

    def post(self, request):
        name = request.POST.get('city')
        if name:
            City.objects.create(title=name)
            cityObj = City.objects.filter(title=name).first()
            cityId = cityObj.id
            cityName = name
            return render(request, 'pop_close.html', locals())
        return render(request, 'pop.html')
