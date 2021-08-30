from django.contrib import admin
from app_rbac import models


admin.site.register(models.UserInfo)
admin.site.register(models.Role)
admin.site.register(models.Permission)
