from django.urls import reverse
from django.utils.safestring import mark_safe
from app_stark.service.StarkModular import StarkHandler, get_choices_text, SearchOption, StarkModelForm
from django import forms
from django.conf import settings as sys
from django.shortcuts import HttpResponse
from django.db import transaction  # 数据锁--事物
from crm.models import Customer, UserInfo, ConsultRecord

"""
客户管理
"""


class PublicForm(StarkModelForm):
    # 对于公户的添加页面视图显示的内容
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['consultant', 'status']  # 排除掉销售顾问、状态


class PrivateForm(StarkModelForm):
    # 对于私户的添加页面视图显示的内容
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['consultant']


class CustomerConfig(StarkHandler):
    """
    所有客户，客户管理
    """

    def display_project(self, obj, is_header=None):
        # 对于咨询项目的 MTM 字段进行自定义展示
        if is_header:
            return '咨询的项目'
        else:
            # 进行跨表查询显示出客户咨询的所有项目（跨表查询MTM字段）
            projects_list = obj.course.all()
            project_list = ['%s' % (row.title) for row in projects_list]
        return mark_safe('<span style="color: red;">||</span>'.join(project_list))

    def display_follow(self, obj=None, is_header=False):
        if is_header:
            return '跟进记录'
        url = reverse('stark:crm_consultrecord_list')
        return mark_safe('<a href="%s?cid=%s">跟进记录</a>' % (url, obj.pk))

    list_display = ['id', 'name', 'tel', display_project,
                    get_choices_text('性别', 'gender'),
                    get_choices_text('状态', 'status'),
                    get_choices_text('来源', 'source'),
                    display_follow,
                    ]
    order_list = ['id']

    search_list = ['name__contains']

    search_group = [
        SearchOption('gender', show_func=lambda field_obj: field_obj[1] + '性', is_multi=False),
        SearchOption('status', is_multi=False),
        SearchOption('source', is_multi=False),
    ]


class PublicCustomerConfig(StarkHandler):
    """
    公户客户管理
    """
    list_display = [StarkHandler.display_checkbox,
                    'id', 'name', 'qq', get_choices_text('性别', 'gender'),
                    get_choices_text('状态', 'status'), 'course',
                    get_choices_text('来源', 'source'),
                    ]

    def get_list_display(self):
        # 公户不允许删除客户，调用父类的配置方法，将默认的删除按钮去掉
        val = super().get_list_display()
        val.remove(StarkHandler.display_del)
        # val.insert(0, StarkHandler.display_checkbox)  # 在0号位置添加多选按钮
        return val

    def multi_apply(self, request):
        # 批量操作申请到私户
        id_list = request.POST.getlist('pk')
        current_user_id = 3
        my_customer = Customer.objects.filter(consultant_id=current_user_id, status=2).count()
        # 提前判断要添加到私户的客户数量是否大于可对接客户总量
        if my_customer == sys.MAX_PRIVATE_CUSTOMER:
            return HttpResponse('您当前对接的客户已达上限，无法再添加')
        elif (my_customer + len(id_list)) > sys.MAX_PRIVATE_CUSTOMER:
            max_length = sys.MAX_PRIVATE_CUSTOMER - my_customer  # 提示最多还能申请进入私户的数量
            return HttpResponse('您当前最多还能申请“　%s　”个客户' % max_length)

        # 开启事物操作，锁定数据，避免抢数据导致被覆盖的情况
        flag = False
        with transaction.atomic():
            origin = Customer.objects.filter(id__in=id_list, consultant__isnull=True).select_for_update()
            if len(origin) == len(id_list):
                Customer.objects.filter(id__in=id_list).update(consultant_id=current_user_id)
                flag = True
        if not flag:
            return HttpResponse('手速太慢，这批客户已经被申请走了！')

    multi_apply.text = '申请到个人'
    action_list = [multi_apply]

    order_list = ['id']

    search_list = ['name__contains']

    search_group = [
        SearchOption('gender', show_func=lambda field_obj: field_obj[1] + '性', is_multi=False),
        SearchOption('status', is_multi=False),
        SearchOption('source', is_multi=False),
    ]

    def get_queryset(self):
        # 公户销售顾问为空
        return self.model_class.objects.filter(consultant__isnull=True)

    model_form_class = PublicForm


class PrivateCustomerConfig(StarkHandler):
    """
    私户客户管理
    """

    def display_follow(self, obj=None, is_header=False):
        if is_header:
            return '跟进记录'
        url = reverse('stark:crm_consultrecord_pri_list')
        return mark_safe('<a href="%s?cid=%s">跟进记录</a>' % (url, obj.pk))

    list_display = [StarkHandler.display_checkbox, 'id', 'name', 'qq', get_choices_text('性别', 'gender'),
                    get_choices_text('状态', 'status'), 'course',
                    get_choices_text('来源', 'source'),
                    display_follow,
                    ]

    def get_list_display(self):
        # 私户不允许删除客户，调用父类的配置方法，将默认的删除按钮去掉
        val = super().get_list_display()
        val.remove(StarkHandler.display_del)
        return val

    def multi_remove(self, request):
        # 批量操作移除客户到公户
        id_list = request.POST.getlist('pk')
        current_user_id = 3
        # 将客户状态为未确认的，并且在当前登陆销售对接客户下的客户移入公户
        Customer.objects.filter(id__in=id_list, status=2, consultant_id=current_user_id).update(consultant_id=None)

    multi_remove.text = '移除到公户'
    action_list = [multi_remove]

    order_list = ['id']

    search_list = ['name__contains']

    model_form_class = PrivateForm

    search_group = [
        SearchOption('gender', show_func=lambda field_obj: field_obj[1] + '性', is_multi=False),
        SearchOption('status', is_multi=False),
        SearchOption('source', is_multi=False),
    ]

    def get_queryset(self):
        # 私户筛选条件为当前客户的销售顾问等于当前登陆用户即可
        current_user_id = 3
        return self.model_class.objects.filter(consultant_id=current_user_id)

    def save(self, form, is_update=False):
        # 私户 添加\编辑 保存时，手动将客户挂到当前登陆销售名下
        current_user_id = 3
        form.instance.consultant = UserInfo.objects.get(id=current_user_id)
        return form.save()


class ConsultRecordConfig(StarkHandler):
    """
    所有客户跟进记录
    """
    list_display = ['id', 'customer', 'date', 'note']
    search_list = ['name__contains']

    def get_queryset(self):
        # 筛选出当前客户的所有跟进记录
        cid = self.request.GET.get('cid')
        if cid:
            return ConsultRecord.objects.filter(customer_id=cid)
        return ConsultRecord.objects


class PriModelForm(forms.ModelForm):
    # 私户 添加功能 表单
    class Meta:
        model = ConsultRecord
        exclude = ['customer', 'consultant']


class PriConsultRecordConfig(StarkHandler):
    """
    私户跟进记录
    """
    list_display = [StarkHandler.display_checkbox,
                    'id', 'customer', 'date', 'note']
    search_list = ['name__contains']

    model_form_class = PriModelForm

    def get_queryset(self):
        # 筛选出当前客户的所有跟进记录
        cid = self.request.GET.get('cid')
        current_user_id = 3
        if cid:
            return ConsultRecord.objects.filter(customer_id=cid, customer__consultant_id=current_user_id)
        return ConsultRecord.objects.filter(customer__consultant_id=current_user_id)

    def save(self, form, is_update=False):
        """
        在添加页面：私户客户跟进记录只需要填写跟进内容，不需要指定客户和销售
        手动设置一个客户id和当前登陆用户id即可
        """
        if not is_update:
            params = self.request.GET.get('_filter')
            cid, num = params.split('=', maxsplit=1)
            form.instance.customer = Customer.objects.get(id=num)  # 设置客户id
            current_user_id = 3  # 当前用户登陆id
            form.instance.consultant = UserInfo.objects.get(id=current_user_id)  # 设置当前跟进记录销售id
        form.save()
