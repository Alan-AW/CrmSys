## **RBAC:Role based user access control**

## 基于角色的用户权限控制

**rbac实现流程：1.用户登陆 --> 2.(3)权限初始化(读取当前用户拥有的所有权限，放入session中) --> 3(2).中间件读取权限信息做权限校验**

**<u>用户所有请求都会先穿过中间件，在中间件中会读取当前用户请求url，如果是白名单的话会直接放行，进入用户登陆校验，然后做权限初始化，将当前用户所拥有的所有权限与菜单信息全部获取写入session。</u>**

*<u>用户再次发出请求，穿过中间件的时候仍然会做权限校验，是否登陆、是否有权限访问......</u>**



## 一、为页面上ModelForm统一添加一个样式：

```python
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
        super(UpdateUserModelForm, self).__init__(*args, **kwargs)  # 执行父类的初始化方法。
        for name, fields in self.fields.items():  # 通过此方式循环出所有生成的对象
            fields.widget.attrs['class'] = 'form-control
```

如果只写上`super(UpdateUserModelForm, self).__init__(*args, **kwargs)`  去执行父类的初始化方法。等于没写。

但是内部加上了自定制的操作之后便获取到了内置的form组件生成的类似与CharField()的对象：为每一个对象都加上了一个 class 属性 

form-control 其中：name 表示所有的字段，fields 表示字段对象，也就是页面上的input标签

## 二、Django模版寻找的顺序：

首先去系统的根目录的templates中查找、如果没有，那么就会根据settings中APP的注册顺序，去每一个APP目录下寻找templates中寻找，需要注意的是重名的情况，可以在每个APP中单独创建一个templates目录，该目录下单独创建与当前APP同名的目录，然后将模版放入其中，这样就避免了重名导致程序报错的可能性。

## 三、ModelForm的使用

单独创建一个目录专门保存独立的ModelForm

```python
form rbac.models import Role
# ModelForm
class RoleModelForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['title']  # 如果直接写成  '__all__'， 表示对所有字段都可以进行操作
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
```

在视图函数中使用

```python
# Views视图函数

# 视图函数中，如果是编辑页面，那么需要让页面中默认展示出当前页面中操作的表的每一个字段在数据库中存储的内容，使用方法：
# roleObj = Role.objects.filter(id=pk).first()
# form = RoleModelForm(instance=roleObj)
# 加上一个参数 instance=roleObj

from form import RoleModelForm
class RoleAdd(View):
    """
    添加角色
    """

    def get(self, request):
        form = RoleModelForm
        return render(request, 'rbac/change.html', locals())

    def post(self, request):
        form = RoleModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:role_list'))
        else:
            return render(request, 'rbac/change.html', locals())

```

模版文件中使用：

```django
<form class="form-horizontal" method="post" novalidate>
    {% csrf_token %}
    {% for field in form %}
    <div class="form-group">
        <label class="col-sm-2 control-label">{{ field.label }}</label>
        <div class="col-sm-8">
            {{ field }}
            <span>{{ field.errors.0 }}</span>
        </div>
    </div>
    {% endfor %}
    <div class="form-group">
        <div class="col-sm-offset-2 col-sm-8">
            <input type="submit" value=" 保 存 " class="btn btn-primary">
        </div>
    </div>
</form>
```

## 四、钩子方法对自定义字段的校验

```python
class UserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = import_string(sys.USER_MODEL_CLASS)
        fields = ['name', 'email', 'roles',
                  'username', 'password', 'confirm_password',
                  'gender', 'phone', 'depart'
                  ]

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
```

对于自定义字段 confirm_password  字段，需要对其进行检测的话可以写上一个函数，函数的  **开头**  以  **clean_**  开始后面跟自定义字段名即可

