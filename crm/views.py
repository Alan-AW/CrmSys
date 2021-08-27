from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from crm.models import *


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

