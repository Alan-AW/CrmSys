from django.db import models


class Department(models.Model):
    title = models.CharField(verbose_name='部门', max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'depart'
        verbose_name = '部门'


class UserInfo(models.Model):
    name = models.CharField(verbose_name='真实姓名', max_length=64)
    gender_choices = (
        (1, '男'),
        (2, '女')
    )
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices, default=1)
    phone = models.CharField(verbose_name='电话', max_length=32)
    email = models.EmailField(verbose_name='邮箱', max_length=64)
    depart = models.ForeignKey(to='Department', verbose_name='所属部门', on_delete=models.CASCADE)
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='登陆密码', max_length=64)

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
