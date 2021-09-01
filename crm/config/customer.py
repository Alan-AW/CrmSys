from app_stark.service.v1 import StarkHandler, get_choices_text, SearchOption


class CustomerHandler(StarkHandler):
    list_display = ['id', 'name', 'qq', get_choices_text('性别', 'gender'),
                    get_choices_text('状态', 'status'), 'course',
                    get_choices_text('来源', 'source'),
                    ]
    order_list = ['id']

    search_list = ['name__contains']

    search_group = [
        SearchOption('gender', show_func=lambda field_obj: field_obj[1] + '性', is_multi=False),
        SearchOption('status', is_multi=False),
        SearchOption('source', is_multi=False),
    ]


class PublicCustomerHandler(StarkHandler):
    list_display = ['id', 'name', 'qq', get_choices_text('性别', 'gender'),
                    get_choices_text('状态', 'status'), 'course',
                    get_choices_text('来源', 'source'),
                    ]
    order_list = ['id']

    search_list = ['name__contains']

    search_group = [
        SearchOption('gender', show_func=lambda field_obj: field_obj[1] + '性', is_multi=False),
        SearchOption('status', is_multi=False),
        SearchOption('source', is_multi=False),
    ]


class PrivateCustomerHandler(StarkHandler):
    list_display = ['id', 'name', 'qq', get_choices_text('性别', 'gender'),
                    get_choices_text('状态', 'status'), 'course',
                    get_choices_text('来源', 'source'),
                    ]
    order_list = ['id']

    search_list = ['name__contains']

    search_group = [
        SearchOption('gender', show_func=lambda field_obj: field_obj[1] + '性', is_multi=False),
        SearchOption('status', is_multi=False),
        SearchOption('source', is_multi=False),
    ]
