from django import forms
from django.utils.module_loading import import_string  # 内置工具，根据字符串进行导入模块
from django.conf import settings as sys
from django.core.exceptions import ValidationError


class UserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = import_string(sys.USER_MODEL_CLASS)
        fields = ['name', 'email', 'roles',
                  'username', 'password', 'confirm_password',
                  'gender', 'phone', 'depart'
                  ]

    def __init__(self, *args, **kwargs):
        """
        统一添加样式
        :param args:
        :param kwargs:
        """
        super(UserModelForm, self).__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs['class'] = 'form-control'

    def clean_confirm_password(self):
        """
        密码一致性检测
        :return:
        """
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('两次输入的密码不一致!')  # 抛出异常
        return confirm_password  # 密码检测通过，返回验证字段信息


class UpdateUserModelForm(forms.ModelForm):
    class Meta:
        model = import_string(sys.USER_MODEL_CLASS)
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        """
        统一添加样式
        :param args:
        :param kwargs:
        """
        super(UpdateUserModelForm, self).__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs['class'] = 'form-control'
