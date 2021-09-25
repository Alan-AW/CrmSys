from CrmSys import settings as sys


def initPermission(userObj, request):
    """
    用户权限初始化
    :param userObj:  当前用户对象
    :param request:   请求相关的所有数据
    :return:
    """
    # 根据当前用户信息获取到所有的权限，然后放入到session中

    permissionQueryset = userObj.roles.filter(permission__isnull=False) \
        .values('permission__id',
                'permission__title',
                'permission__url',
                'permission__name',

                'permission__pid_id',
                'permission__pid__title',
                'permission__pid__url',

                'permission__menu_id',
                'permission__menu__title',
                'permission__menu__icon'
                ).distinct()  # 获取到所有权限(url) 并去重
    # 获取到所有的权限 + 菜单信息 并且写入session
    permissionDict = {}
    menuDict = {}
    for item in permissionQueryset:
        permissionDict[item['permission__name']] = {
            'id': item['permission__id'],
            'title': item['permission__title'],
            'url': item['permission__url'],

            'pid': item['permission__pid_id'],
            'p_title': item['permission__pid__title'],
            'p_url': item['permission__pid__url']
        }
        menuId = item['permission__menu_id']
        if not menuId:
            continue
        node = {'id': item['permission__id'], 'title': item['permission__title'], 'url': item['permission__url']}
        if menuId in menuDict:
            menuDict[menuId]['children'].append(node)
        else:
            menuDict[menuId] = {
                'title': item['permission__menu__title'],
                'icon': item['permission__menu__icon'],
                'children': [node, ]
            }

    request.session[sys.PERMISSION_SESSION_KEY] = permissionDict
    request.session[sys.MENU_SESSION_KEY] = menuDict


'''
    permissionList： 首先通过MTM多对多关系获取到所有的角色再通过映射permission双下划线再次跨表反向查询到需要的url
    问题一：
        一个用户拥有多个角色，
        一个角色拥有多个权限
    解决：
        去重： .distinct()
    问题二：
        如果某一个角色没有任何权限(权限为null)，但是某个人拥有的多个角色中包含了这个没有权限的角色怎么办？
    解决：
        将：权限查询语句：
            userObj.roles.all().xxxxxx
        改为：
            userObj.roles.filter(permission__isnull=False)
        这样就能保证获取到所有的权限url
    '''
