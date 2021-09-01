from app_rbac import models
from django import forms
from django.utils.safestring import mark_safe
from app_rbac.forms.base import BootStrapModelForm


def get_icon():
    ICON_LIST = [
        ['fa-hand-scissors-o', '<i aria-hidden="true" class="fa fa-hand-scissors-o"></i>'],
        ['fa-hand-spock-o', '<i aria-hidden="true" class="fa fa-hand-spock-o"></i>'],
        ['fa-hand-stop-o', '<i aria-hidden="true" class="fa fa-hand-stop-o"></i>'],
        ['fa-handshake-o', '<i aria-hidden="true" class="fa fa-handshake-o"></i>'],
        ['fa-hard-of-hearing', '<i aria-hidden="true" class="fa fa-hard-of-hearing"></i>'],
        ['fa-hashtag', '<i aria-hidden="true" class="fa fa-hashtag"></i>'],
        ['fa-hdd-o', '<i aria-hidden="true" class="fa fa-hdd-o"></i>'],
        ['fa-headphones', '<i aria-hidden="true" class="fa fa-headphones"></i>'],
        ['fa-heart', '<i aria-hidden="true" class="fa fa-heart"></i>'],
        ['fa-heart-o', '<i aria-hidden="true" class="fa fa-heart-o"></i>'],
        ['fa-heartbeat', '<i aria-hidden="true" class="fa fa-heartbeat"></i>'],
        ['fa-history', '<i aria-hidden="true" class="fa fa-history"></i>'],
        ['fa-home', '<i aria-hidden="true" class="fa fa-home"></i>'],
        ['fa-hotel', '<i aria-hidden="true" class="fa fa-hotel"></i>'],
        ['fa-hourglass', '<i aria-hidden="true" class="fa fa-hourglass"></i>'],
        ['fa-hourglass-1', '<i aria-hidden="true" class="fa fa-hourglass-1"></i>'],
        ['fa-hourglass-2', '<i aria-hidden="true" class="fa fa-hourglass-2"></i>'],
        ['fa-hourglass-3', '<i aria-hidden="true" class="fa fa-hourglass-3"></i>'],
        ['fa-hourglass-end', '<i aria-hidden="true" class="fa fa-hourglass-end"></i>'],
        ['fa-hourglass-half', '<i aria-hidden="true" class="fa fa-hourglass-half"></i>'],
        ['fa-hourglass-o', '<i aria-hidden="true" class="fa fa-hourglass-o"></i>'],
        ['fa-hourglass-start', '<i aria-hidden="true" class="fa fa-hourglass-start"></i>'],
        ['fa-i-cursor', '<i aria-hidden="true" class="fa fa-i-cursor"></i>'],
        ['fa-id-badge', '<i aria-hidden="true" class="fa fa-id-badge"></i>'],
        ['fa-id-card', '<i aria-hidden="true" class="fa fa-id-card"></i>'],
        ['fa-id-card-o', '<i aria-hidden="true" class="fa fa-id-card-o"></i>'],
        ['fa-image', '<i aria-hidden="true" class="fa fa-image"></i>'],
        ['fa-mail-reply-all', '<i aria-hidden="true" class="fa fa-mail-reply-all"></i>'],
        ['fa-reply', '<i aria-hidden="true" class="fa fa-reply"></i>'],
        ['fa-reply-all', '<i aria-hidden="true" class="fa fa-reply-all"></i>'],
        ['fa-retweet', '<i aria-hidden="true" class="fa fa-retweet"></i>'],
        ['fa-wrench', '<i aria-hidden="true" class="fa fa-wrench"></i>']]
    for item in ICON_LIST:
        item[1] = mark_safe(item[1])
    return ICON_LIST


class MenuModelForm(forms.ModelForm):
    """
    一级菜单编辑表单
    """

    class Meta:
        model = models.Menu
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.RadioSelect(
                choices=get_icon(),
                attrs={'class': 'clearfix'}
            )
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
