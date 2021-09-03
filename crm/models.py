from django.db import models
from app_rbac.models import UserInfo as RbacUserInfo


class Department(models.Model):
    title = models.CharField(verbose_name='部门', max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'depart'
        verbose_name = '部门'


class UserInfo(RbacUserInfo):
    name = models.CharField(verbose_name='真实姓名', max_length=64)
    gender_choices = (
        (1, '男'),
        (2, '女')
    )
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices, default=1)
    phone = models.CharField(verbose_name='电话', max_length=32)
    depart = models.ForeignKey(to='Department', verbose_name='所属部门', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'
        verbose_name = '员工'


class Project(models.Model):
    title = models.CharField(verbose_name='项目', max_length=64)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'project'
        verbose_name = '项目'


class City(models.Model):
    name = models.CharField(verbose_name='地区', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'city'
        verbose_name = '地区'


class Company(models.Model):
    """
    分公司
    """
    city = models.ForeignKey(to='City', verbose_name='地区', on_delete=models.CASCADE)
    project = models.ForeignKey(to='Project', verbose_name='项目', on_delete=models.CASCADE)
    semester = models.IntegerField(verbose_name='期数', default=1)
    price = models.IntegerField(verbose_name='项目款', default=1000000)
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期', null=True, blank=True)
    # 项目经理和负责人关联到的用户表，此处可以进行筛选 (也可以使用Q对象进行复杂的筛选)：
    # limit_choices_to={'depart_id__in': [1,3]}
    # limit_choices_to={'depart_id': 1}
    # limit_choices_to={'depart__title': '管理层'}
    manger = models.ForeignKey(verbose_name='项目经理', to='UserInfo', related_name='manager',
                               on_delete=models.CASCADE, limit_choices_to={'depart__title': '管理层'})
    principal = models.ManyToManyField(verbose_name='负责人', to='UserInfo', related_name='principal',
                                       limit_choices_to={'depart__title': '管理层'})

    # manger = models.ForeignKey(verbose_name='项目经理', to='UserInfo', related_name='manager', on_delete=models.CASCADE)
    # principal = models.ManyToManyField(verbose_name='负责人', to='UserInfo', related_name='principal')

    memo = models.CharField(verbose_name='项目说明', max_length=256, blank=True, null=True)

    def __str__(self):
        return self.city

    class Meta:
        db_table = 'company'
        verbose_name = '分公司'


class Customer(models.Model):
    """
    客户表
    """
    name = models.CharField(verbose_name='姓名', max_length=32)
    qq = models.CharField(verbose_name='联系方式', max_length=64, unique=True, help_text='QQ号/微信/手机号')
    status_choices = [
        (1, "已确认"),
        (2, "未确认")
    ]
    status = models.IntegerField(verbose_name="状态", choices=status_choices, default=2)
    gender_choices = ((1, '男'), (2, '女'))
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)

    source_choices = [
        (1, "qq群"),
        (2, "内部转介绍"),
        (3, "官方网站"),
        (4, "百度推广"),
        (5, "360推广"),
        (6, "搜狗推广"),
        (7, "腾讯课堂"),
        (8, "广点通"),
        (9, "高校宣讲"),
        (10, "渠道代理"),
        (11, "51cto"),
        (12, "智汇推"),
        (13, "网盟"),
        (14, "DSP"),
        (15, "SEO"),
        (16, "裙带"),
        (17, "其它"),
    ]
    source = models.SmallIntegerField('客户来源', choices=source_choices, default=1)

    referral_from = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        verbose_name="转介绍自客户",
        help_text="若此客户是转介绍自内部人员,请在此处选择内部人员姓名",
        related_name="internal_referral",
        on_delete=models.SET_NULL
    )

    course = models.ManyToManyField(verbose_name="咨询项目", to="Project")
    consultant = models.ForeignKey(verbose_name="项目顾问", to='UserInfo', related_name='consultant',
                                   null=True, blank=True,
                                   limit_choices_to={'depart__title': '销售部'},
                                   on_delete=models.SET_NULL
                                   )
    education_choices = (
        (1, '重点大学'),
        (2, '普通本科'),
        (3, '独立院校'),
        (4, '民办本科'),
        (5, '大专'),
        (6, '民办专科'),
        (7, '高中'),
        (8, '其他')
    )
    education = models.IntegerField(verbose_name='学历', choices=education_choices, blank=True, null=True, )
    graduation_school = models.CharField(verbose_name='毕业学校', max_length=64, blank=True, null=True)
    major = models.CharField(verbose_name='所学专业', max_length=64, blank=True, null=True)

    experience_choices = [
        (1, '在校生'),
        (2, '应届毕业'),
        (3, '半年以内'),
        (4, '半年至一年'),
        (5, '一年至三年'),
        (6, '三年至五年'),
        (7, '五年以上'),
    ]
    experience = models.IntegerField(verbose_name='工作经验', blank=True, null=True, choices=experience_choices)
    work_status_choices = [
        (1, '在职'),
        (2, '无业')
    ]
    work_status = models.IntegerField(verbose_name="职业状态", choices=work_status_choices, default=1, blank=True,
                                      null=True)
    company = models.CharField(verbose_name="目前就职公司", max_length=64, blank=True, null=True)
    salary = models.CharField(verbose_name="当前薪资", max_length=64, blank=True, null=True)

    date = models.DateField(verbose_name="咨询日期", auto_now_add=True)
    last_consult_date = models.DateField(verbose_name="最后跟进日期", auto_now_add=True)

    def __str__(self):
        return "姓名:{0},联系方式:{1}".format(self.name, self.qq, )

    class Meta:
        db_table = 'customer'


class ConsultRecord(models.Model):
    """
    客户跟进记录
    """
    customer = models.ForeignKey(verbose_name='所咨询客户', to='Customer', on_delete=models.CASCADE)
    consultant = models.ForeignKey(verbose_name='跟踪人', to='UserInfo', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='跟进日期', auto_now_add=True)
    note = models.TextField(verbose_name='内容/说明')

    class Meta:
        db_table = 'consultrecord'

    def __str__(self):
        return self.customer


class PaymentRecord(models.Model):
    """
    支付记录
    """
    pass
