from collections import OrderedDict
from django.conf import settings as sys
from django.utils.module_loading import import_string  # 内置工具，根据字符串进行导入模块
from django.urls import URLResolver, URLPattern
import re

"""
自动发现项目中的url方法
"""


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
            if isinstance(item, URLPattern):  # 非路由分发
                if not item.name:
                    continue
                name = item.name if not pre_namespace else "%s:%s" % (pre_namespace, item.name)
                url = pre_url + item.pattern.regex.pattern
                url = url.replace('^', '').replace('$', '')
                if self.check_url_exclude(url):
                    continue
                url_ordered_dict[name] = {'name': name, 'url': url}
            elif isinstance(item, URLResolver):  # 路由分发, 递归
                if pre_namespace:
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
