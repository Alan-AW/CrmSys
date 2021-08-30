from django import forms
from app_rbac.models import Role


class RoleModelForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['title']  # 如果直接写成  '__all__'， 表示对所有字段都可以进行操作
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
