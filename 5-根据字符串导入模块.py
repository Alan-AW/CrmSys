"""
Form & ModelForm 的区别
Form 字段需要自定义
ModelForm 字段直接使用数据库中的数据
Formset ---
"""

# 反射：根据字符串导入模块并找到类
# Python 提供 （自定义）
from importlib import import_module

path = '5-xxx.Foo'
model_path, class_name = path.split('.', maxsplit=1)
m = import_module(model_path)
# 找到Foo类
cls = getattr(m, class_name)
# 实例化
obj = cls('old boy')
# 执行
obj.func()  # old boy

# django提供 的 内置 模块
from django.utils.module_loading import import_string

v = import_string('5-xxx.Foo')
obj1 = v('young boy')  # 实例化
obj1.func()  # young boy

"""
首先定义好，处理函数类init接受参数。
py_path_str 上传py文件名称。例如abc，py的命名是abc.py文件
file_path_str 上传文件路径名。例如user_file，上传的py文件在user_file文件下
fun_name 上传py文件中的方法或函数名

自动导入模块
def read():
    math = importlib.import_module(py_path_str, file_path_str)
自动导入方法或函数
def read():
    math = importlib.import_module(py_path_str, file_path_str)
    a_class = getattr(math, func_name)()

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
这个功能的强大之处就在于遵循了开放封闭原则：*对代码封闭，对配置开放。*
使得程序的可扩展性变强
可以通过配置文件实现调用对应的方法
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""

"""

# 开放封闭原则示例：
# settings.py(配置文件) 中：
PATH_LIST = [
    'make.XX.Foo',
    'make.XX.Bar',
    'make.XX.Obj',
]

# 主程序
for path in settings.PATH_LIST:
    model_path, class_name = path.split('.', maxsplit=1)
    m = import_module(model_path)
    # 找到Foo类
    cls = getattr(m, class_name)
    # 实例化
    obj = cls()
    # 执行
    obj.func()  # old boy

# 对应 make.py 中
class Foo():
    def __init__(self, mas):
        self.msg = msg
    def func():
        pass

class Foo():
    def __init__(self, mas):
        self.msg = msg
    def func():
        pass

class Foo():
    def __init__(self, mas):
        self.msg = msg
    def func():
        pass
    
    ......
    
后期需要扩展功能的时候只需要在make.py中写对应的执行方法，然后将方法写入配置文件中就可以自动执行
不需要到每个地方都改动源码，那样是违背了开放封闭原则的做法。
"""