"""
员工管理配置文件
"""
from django.urls import reverse
from django.utils.safestring import mark_safe
from app_stark.service.StarkModular import StarkHandler, get_choices_text, SearchOption, StarkModelForm
from django import forms
from django.conf import settings as sys
from django.shortcuts import HttpResponse
from django.db import transaction  # 数据锁--事物
from crm.models import Customer, UserInfo, ConsultRecord


# 员工考勤管理
class StaffRecordConfig(StarkHandler):
    list_display = [StarkHandler.display_checkbox, 'id', 'name', 'should', 'later', 'leave',
                    'ask_leave', 'fine', 'actual'
                    ]
    order_list = ['id']
    search_list = ['name__name__contains']
    # search_group = [
    #     SearchOption('name', show_func=lambda field_obj: field_obj[1] + '同事'),
    # ]
