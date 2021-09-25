## **RBAC:Role based user access control**

## 基于角色的用户权限控制

**rbac实现流程：1.用户登陆 --> 2.(3)权限初始化(读取当前用户拥有的所有权限，放入session中) --> 3(2).中间件读取权限信息做权限校验**

**<u>用户所有请求都会先穿过中间件，在中间件中会读取当前用户请求url，如果是白名单的话会直接放行，进入用户登陆校验，然后做权限初始化，将当前用户所拥有的所有权限与菜单信息全部获取写入session。</u>**

*<u>用户再次发出请求，穿过中间件的时候仍然会做权限校验，是否登陆、是否有权限访问......</u>**



## 一、自动发现项目中的URL

## 实现思路：

>   **在配置文件settings中，配置项：ROOT_URLCONF = 'CrmSys.urls'，便是项目的根URL地址，其他所有的路由都是在这个地方进行分发的。根据ROOT_URLCONFIG配置项中的urlpatterns列表中的项，判断其类型，在其内部会根据传递的参数不同实例化生成不同的对象：**
>
>   **RegexURLResolver对象   和   RegexURLRPattern对象** 
>
>   **如果是RegexURLResolver对象，那么就表示该路由是进行了路由分发的，如果是RegexURLRPattern对象，那么当前路由即根路由；**

#### settings.py：

```python
ROOT_URLCONF = 'CrmSys.urls'  # 根路由的路径
```

#### CrmSys.urls：

```python
urlpatterns = [
    # 用户登陆&退出
    path('login/', Login.as_view(), name='login'),  # RegexURLRPattern
    path('logout/', Logout.as_view(), name='logout'),  # RegexURLRPattern
    path('welcome/', Welcome.as_view(), name='welcome'),  # RegexURLRPattern
    path('no_permission_html/', NoPermissionHtml.as_view()),  # RegexURLRPattern
    # stark 组件应用
    path('stark/', site.urls),  # RegexURLResolver
    # rbac 组件应用
    path('rbac/', include('app_rbac.urls', namespace='rbac')), # RegexURLResolver

]
```

# 二、获取项目中所有URL

```python
from django.urls import URLResolver, URLPattern

from django.conf import settings as sys
from django.utils.module_loading import import_string

class AutoFindUrl:
    def check_url_exclude(self, url):
        """
        白名单设置;排除一些特定的url的查找
        :param url:
        :return:
        """
        for regex in sys.AUTO_DISCOVER_EXCLUDE:
            if re.match(regex, url):
                return True

    def recursion_urls(self, pre_namespace, pre_url, url_patterns, url_ordered_dict):
        """
        :param pre_namespace: namespace的前缀， 以后用于拼接name
        :param pre_url: url的前缀， 以后用于拼接url
        :param url_patterns: 用于循环的路由， 路由关系列表
        :param url_ordered_dict: 用于保存递归中获取的所有路由，有序字典
        :return:
        """
        for item in url_patterns:
            if isinstance(item, URLPattern):  # 匹配成功表示非路由分发
                if not item.name:
                    continue
                name = item.name if not pre_namespace else "%s:%s" % (pre_namespace, item.name)
                url = pre_url + item.pattern.regex.pattern
                url = url.replace('^', '').replace('$', '')  # 将起止和终止符替换掉
                if self.check_url_exclude(url):  # 排除掉特定的url
                    continue
                url_ordered_dict[name] = {'name': name, 'url': url}
            elif isinstance(item, URLResolver):  # 匹配成功表示进行了路由分发, 递归获取所有的URL
                if pre_namespace:  # 对路由分发的 namespace 进行拼接
                    # 再次判断分发之后的路由有没有namespace，有就用自己的namespace，没有就用父级的namespace
                    namespace = "%s:%s" % (pre_namespace, item.namespace) if item.namespace else item.namespace
                else:
                    namespace = item.namespace if item.namespace else None
                self.recursion_urls(namespace, pre_url + item.pattern.regex.pattern, item.url_patterns, url_ordered_dict)

    def get_all_url_dict(self):
        """
        自动发现项目中的URL(必须有  name  别名)
        :return: 所有url的有序字典
        """
        url_ordered_dict = OrderedDict()  # {'rbac:menu_list': {name:'rbac:menu_list', url: 'xxx/xxx/menu_list'}}
        md = import_string(sys.ROOT_URLCONF)  # 根据字符串的形式去导入一个模块，在settings中 ROOT_URLCONF 指向的就是项目根路由的文件地址
        self.recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)  # 递归的获取所有的url
        return url_ordered_dict

```

#### 结果：

```python
{
    'rbac:menu_list': {'name': 'rbac:menu_list', 'url': '/menu/list/'},
    'rbac:menu_add': {'name': 'rbac:menu_add', 'url': '/menu/add/'},
}
```

