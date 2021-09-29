## **STARK组件:**帮助开发者对数据表快速进行 增删改查+ 的功能组件

## 一、基本逻辑

#### 1.通过技术点准备，将三个技术点串联起来可以得到一个实现stark组件的基本逻辑：

1.1--启动程序前执行一段脚本

```python
# 在APP下的app.py文件中的APPconfig类中，定义一个方法：
def ready(self):
	autodiscover_modules('文件名')
# 在程序启动的时候会去执行这个ready方法，该方法自动引入了一个文件，并且自动执行了这个文件
```

**那么在执行这个ready方法的时候，Django程序会去每个注册的APP下寻找这个文件并执行**

1.2--额外定义一个<u>xxx文件</u>，在这个文件中生成一个列表，该列表用于动态生成url路由

```python
class StarkHandler(object):
    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'
    
    def register(self, model_class, handler_class=None, prev=None):
        # 使用stark组件时调用的方法，获取到传递过来的参数
        """
        model_class: 要操作的表对象(类)
        handler_class: 对表进行增删改查操作的类
        prev: 生成路由的前缀
        """
        self._registry.append({
            'model_class': model_class,
            'handler': handler_class(self, model_class, prev),
            'prev': prev
        })
    
    def get_urls(self):
        # 动态生成URL
        patterns = []
        for item in self._registry:
            model_class = item['model_class']
            handler = item['handler']
            prev = item['prev']
            app_name, model_name = model_class._meta.app_label, model_class._meta.model_label
            if prev:
                patterns.append(path('%s/%s/%s/' % (app_name, model_name, prev), (handler.get_urls(), None, None)))
                # (handler.get_urls(), None, None) 是再次进行了路由分发，这是一个元祖，第一个参数调用的默认的stark组件提				 供的视图函数操作类中的路由分发，返回的是一个列表，
            else:
                patterns.append(path('%s/%s/' % (app_name, model_name), (handler.get_urls(), None, None)))
        return patterns
        
    @property
    def urls(self):
        #　路由中调用的方法
        return (self.get_urls(), self.app_name, self.namespace)
    
site = StarkHandler()
```

1.3--在ready方法中执行的文件内导入这个site，并且修改掉site中的值

```python
from xxx import site

site._registry.append('app01')
```

1.4--假设有多个APP，且都定义了一个ready方法执行的脚本文件名，同时在这些文件中都对site._registry的值进行了添加

```python
from app01.xxx imnport site

site._registry.append('app0N')
```

以上操作都是在Django项目加载路由之前完成的，那么根据路由分发的本质，就可以在Django项目读取路由的时候去获取到这个_registry的值，做一个路由分发

```python
# 在项目根路由当中
from xxx import site

patterns = [
    path('stark/', site.urls),
]
# 此时可以测试出，Django运行起来之后访问以下链接：
"""
127.0.0.1:8001/stark/app01/
.
.
127.0.0.1:8001/stark/app0N/
"""
```

**那么此时整个stark组件的原理基本完成**

