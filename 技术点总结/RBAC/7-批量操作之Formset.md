## **RBAC:Role based user access control**

## 基于角色的用户权限控制

**rbac实现流程：1.用户登陆 --> 2.(3)权限初始化(读取当前用户拥有的所有权限，放入session中) --> 3(2).中间件读取权限信息做权限校验**

**<u>用户所有请求都会先穿过中间件，在中间件中会读取当前用户请求url，如果是白名单的话会直接放行，进入用户登陆校验，然后做权限初始化，将当前用户所拥有的所有权限与菜单信息全部获取写入session。</u>**

*<u>用户再次发出请求，穿过中间件的时候仍然会做权限校验，是否登陆、是否有权限访问......</u>**

### 一、表结构设计

​    Permission <-------MTM-------> Role <-------MTM-------> User
​    *权限表中name字段表示的是每个权限(URL)的别名，必须要加上 条件：

## 一、Formset

> **对于数据库中的一行数据可以使用Form和ModelForm来进行验证，即对一个表单进行验证**
>
> **Formset是对多个表单进行批量操作，对多行数据进行批量验证**

**实现方法：**# 对于后台

```python

from django import forms
form django.forms import formset_factory

# 首先自定义一个Form表单
class Formset(forms.Form):
    ....
    # 5个字段
    pass

# 视图中
class MultiAdd(View):
    def __init__():
    	self.formset_class = formset_factory(Formset, extra=5) 
    def get(request):
        formset = self.formset_class()
    	return render(request, 'multi.html', locals())
    def post(request):
        formset = generate_formset_class(data=request.POST)  # 这个formset对象是一个列表包含了一个个的form对象
        # [form(字段，错误), form(字段，错误), form(字段，错误), form(字段，错误),]
        if formset.is_valid():
            object_list = []  # 要添加的数据
            post_row_list = formset.cleaned_data  # 这个对象在formset中保存的是提交到后台的数据（字典套字典）
            # {{字段数据, 错误信息}, {字段数据, 错误信息}, {字段数据, 错误信息}}
            # formset对象与formset.cleaned_data对象是按照索引进行一一对应关系
            # 在源码中，在循环数据的时候从0号索引循环到最后索引，就可以实现对formset.cleaned_data中的数据进行操作
            # 即：下列循环中的 i 代表了字典中嵌套的字典，如果检测到某个字段的错误信息，那么直接将formset.errors[i]设置成				错误提示信息即可精确到某个字段的错误信息展示
            # ****注意： 1.formset.cleaned_data[i] 与 2.formset.errors[i] 是互斥的 ！！！！！！！！！！！！！！！
            # 1.表示formset提交过来的一行数据；2.表示整个formset中出现了错误，只要出现了错误那么第二次循环的时候便读取不				到 formset.cleaned_data 中的信息了，因为上一轮检测没有通过，直接被拦截掉了，
            # 实际上每次循环的时候都会去 formset.cleaned_data 中获取到最新的数据，也就是说每调用一次都会去								formset.cleaned_data 中重新获取一次！！！！！！！！！！！！！
            # 所以为了保证数据的完整性，需要提前将传递到后端的数据保存到一个变量中，循环的时候直接去这个变量中获取数据。
            has_error = False
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_obj = Permission(**row_dict)
                    new_obj.validate_unique()
                    object_list.append(new_obj)  # 检测通过直接append到批量添加的数据中然后批量添加
                except Exception as e:
                    has_error = True
                    formset.errors[i].update(e)
                    generate_formset = formset
            if not has_error:
                Permission.objects.bulk_create(object_list, batch_size=100)  # 没有错误信息的时候直接批量添加操作
        else:
            generate_formset = formset
```

**实现方法：**# 对于前端

```django
{% for form in formset %}
	{% for field in form %}
	    {{ field }}
	{% endfor %}    
{% endfor %}

{# 这样便会在页面中生成5个form表单，如果嵌套到一个表格内进行展示那么就会出现多行数据： #}

<form>
    {% csrf_token %}
    {{ formset.management_form }}
    <table>
        <thead>
            <tr rowspan="5">批量添加</tr>
        </thead>
        <tbody>
            {% for form in formset %}
                <tr>
                    {% for field in form %}
                        <td>
                            {{ field }}
                        </td>
                    {% endfor %}  
                </tr>
            {% endfor %}
        </tbody>
</table>
</form>


```



## 二、自动发现项目中的URL

