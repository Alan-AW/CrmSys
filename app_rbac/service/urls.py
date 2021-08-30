from django.urls import reverse
from django.http import QueryDict


def memoryUrl(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的url，替代模版中的url(url携带参数)
    :param request:
    :param name:
    :return:
    """
    basicUrl = reverse(name, args=args, kwargs=kwargs)
    if not request.GET:  # 当前url中无参数直接返回默认url
        return basicUrl
    queryDict = QueryDict(mutable=True)
    queryDict['_filter'] = request.GET.urlencode()
    oldSearchUrl = queryDict.urlencode()  # 打包（转义）
    return "%s?%s" % (basicUrl, oldSearchUrl)


def memoryReverse(request, name, *args, **kwargs):
    """
    反向生成URL跳转回原地址：
        1.将原来的URL中的搜索条件获取到 _filter
        2.通过reverse生成原来的URL
    将menu操作中的生成url方法封装在此，便于多次调用
    :param request: request
    :param name:  reverse参数
    :param args:  编辑和修改需要的ID
    :param kwargs:  同上
    :return:  返回一个携带参数的url跳转链接
    """
    url = reverse(name, args=args, kwargs=kwargs)
    originParams = request.GET.get('_filter')
    return "%s?%s" % (url, originParams) if originParams else url
