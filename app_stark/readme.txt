stark组件使用文档

1. 拷贝app_stark到任何系统
2. 目标项目中注册app_stark： 'app_stark.apps.AppStarkConfig',
3. 目标app的根目录中创建stark.py文件
4. 配置路由信息：
    from app_stark.service.StarkModular import site
    path('stark/', site.urls),
5. 自定制使用stark组件，进行快速的增删改查
6. 组件内部扩展：
    list_display = list()  # 自定义列的展示内容
    has_add_btn = True  # 是否显示 添加 按钮
    order_list = list()  # 排序规则
    search_list = list()  # 默认查询方式
        search_list = ['字段名__contains']  # 模糊搜索
    action_list = list()  # 批量操作选项
        multi_apply.text = '申请到个人'  # APP中 重写批量操作下拉框显示文本并加入到action_list
    search_group = list()  # 组合搜索组默认配置
        search_group = [  # 组合搜索统一写法、使用方法
            SearchOption('gender', show_func=lambda field_obj: field_obj[1] + '性', is_multi=False),
            ...
        ]
    def display_checkbox(self, obj, is_header=None):  # 批量操作的checkbox展示
    def display_edit(self, obj, is_header=None):  # 实现自定制操作栏(表头与内容)
    def display_del(self, obj, is_header=None):  # 实现自定制删除栏(表头与内容)
    def changelist_view(self, request, *args, **kwargs)  # 默认展示页面渲染
    def save(self, form, is_update=False)  # 所有form保存调用的方法
        例：！！！！！表单传递到后台的所有数据都保存在对象的instance中！！！！！
        def save(self, form, is_update=False):
            # 私户 添加\编辑 保存时，手动将客户挂到当前登陆销售名下
            current_user_id = 3
            form.instance.consultant = UserInfo.objects.get(id=current_user_id)
            return form.save()

    def get_urls(self):  # 默认生成增删改查四条路由，重写可以删除不需要的功能
    def extra_urls(self):  # 增加路由功能的钩子函数
    def get_choices_text(title, field):  # 为数据库多字段的choices字段自定义获取文本内容进行展示以供选择


