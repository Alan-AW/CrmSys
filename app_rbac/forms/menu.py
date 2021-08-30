from app_rbac import models
from django import forms
from django.utils.safestring import mark_safe
from app_rbac.forms.base import BootStrapModelForm


class MenuModelForm(forms.ModelForm):
    """
    一级菜单编辑表单
    """

    class Meta:
        model = models.Menu
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.RadioSelect(choices=[
                ['fa-file-zip-o', mark_safe('<i class="fa fa-file-zip-o" aria-hidden="true"></i>')],
                ['fa-gear', mark_safe('<i class="fa fa-gear" aria-hidden="true"></i>')],
                ['fa-snowflake-o', mark_safe('<i class="fa fa-snowflake-o" aria-hidden="true"></i>')],
                ['fa-vcard', mark_safe('<i class="fa fa-vcard" aria-hidden="true"></i>')],
                ['fa-vcard', mark_safe('<i class="fa fa-vcard" aria-hidden="true"></i>')],
                ['fa-window-close', mark_safe('<i class="fa fa-window-close" aria-hidden="true"></i>')],
                ['fa-wpexplorer', mark_safe('<i class="fa fa-wpexplorer" aria-hidden="true"></i>')],
                ['fa-bell', mark_safe('<i class="fa fa-bell" aria-hidden="true"></i>')],
                ['fa-bomb', mark_safe('<i class="fa fa-bomb" aria-hidden="true"></i>')],
                ['fa-calendar-times-o', mark_safe('<i class="fa fa-calendar-times-o" aria-hidden="true"></i>')],
                ['fa-camera', mark_safe('<i class="fa fa-camera" aria-hidden="true"></i>')],
                ['fa-child', mark_safe('<i class="fa fa-child" aria-hidden="true"></i>')],
                ['fa-cogs', mark_safe('<i class="fa fa-cogs" aria-hidden="true"></i>')],
                ['fa-comment', mark_safe('<i class="fa fa-comment" aria-hidden="true"></i>')],
                ['fa-dashboard', mark_safe('<i class="fa fa-dashboard" aria-hidden="true"></i>')],
                ['fa-envelope', mark_safe('<i class="fa fa-envelope" aria-hidden="true"></i>')],
                ['fa-film', mark_safe('<i class="fa fa-film" aria-hidden="true"></i>')],
                ['fa-folder-open', mark_safe('<i class="fa fa-folder-open" aria-hidden="true"></i>')],
                ['fa-headphones', mark_safe('<i class="fa fa-headphones" aria-hidden="true"></i>')],
                ['fa-heart', mark_safe('<i class="fa fa-heart" aria-hidden="true"></i>')],
                ['fa-leaf', mark_safe('<i class="fa fa-leaf" aria-hidden="true"></i>')],
                ['fa-power-off', mark_safe('<i class="fa fa-power-off" aria-hidden="true"></i>')],
                ['fa-arrows-alt', mark_safe('<i class="fa fa-arrows-alt" aria-hidden="true"></i>')],
                ['fa-first-order', mark_safe('<i class="fa fa-first-order" aria-hidden="true"></i>')],
                ['fa-first-order', mark_safe('<i class="fa fa-first-order" aria-hidden="true"></i>')],
                ['fa-first-order', mark_safe('<i class="fa fa-first-order" aria-hidden="true"></i>')],
            ])
        }


"""
    在菜单页面选择图标
    1. 引入 from django.utils.safestring import mark_safe 
        Django默认标签语言是不安全的，会自动转义为字符串在界面中展示 mark_safe 表示不需要转义直接展示
    2. 使用widgets插件自定义样式
    3. 使用RadioSelect方法将图标的class属性与图标样式标签放在列表中作为展示和选择。
"""


class SecondMenuModelForm(BootStrapModelForm):
    """
    二级菜单编辑表单
    """

    class Meta:
        model = models.Permission
        # fields = ['title', 'url', 'name', 'menu']
        exclude = ['pid']  # 去掉 pid 字段  结果同上


class PermissionModelForm(BootStrapModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'name', 'url']


class MultiAddPermissionForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '------------')],
        required=False
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '------------')],
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True
        ).values_list('id', 'title')


class MultiEditPermissionForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '------------')],
        required=False
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '------------')],
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True
        ).values_list('id', 'title')

