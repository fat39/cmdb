__author__ = 'Administrator'
table_config = [
    {
        'q': None,         # 数据查询字段
        'title': '选择',     # 显示标题
        'display': True,   # 是否显示
        'text': {
            'tpl': "<input type='checkbox' value='{n1}' />",
            'kwargs': {'n1': '@id'}
        },
        'attrs':{'nid':'@id'}

    },
    {
        'q': 'id',
        'title': 'ID',
        'display': False,
        'text': {
            'tpl': "{n1}",
            'kwargs': {'n1': '@id'}
        },
        'attrs':{'k1':'v1','k2':'@id'}
    },
    {
        'q': 'device_type_id',
        'title': '资产类型',
        'display': True,
        'text': {
            'tpl': "{n1}",
            'kwargs': {'n1': '@@device_type_choices'}
        },
        'attrs':{'k1':'v1','origin':'@device_type_id','edit-enable':'true','edit-type':'select','global_key':'device_type_choices','name':'device_type_id'}
    },
    {
        'q': 'device_status_id',
        'title': '状态',
        'display': True,
        'text': {
            'tpl': "{n1}",
            'kwargs': {'n1': '@@device_status_choices'}
        },
        'attrs':{'name':'device_status_id','edit-enable':'true','origin': '@device_status_id','edit-type':'select','global_key':'device_status_choices' }
    },
    {
        'q': 'cabinet_num',
        'title': '机柜号',
        'display': True,
        'text': {
            'tpl': "{n1}",
            'kwargs': {'n1': '@cabinet_num'}
        },
        'attrs':{'name':'cabinet_num','k1':'v1','k2':'@id','edit-enable':'true'}
    },
    {
        'q': 'idc_id',
        'title': '机房',
        'display': False,
        'text': {},
        'attrs':{}
    },
    {
        'q': 'idc__name',
        'title': '机房',
        'display': True,
        'text': {
            'tpl': "{n1}",
            'kwargs': {'n1': '@idc__name'}
        },
        'attrs':{'name':'idc_id','k1':'v1','origin':'@idc_id','edit-enable':'true','edit-type':'select','global_key':'idc_choices'}
    },
    # 页面显示：标题：操作；删除，编辑：a标签
    {
        'q': None,
        'title': '操作',
        'display': True,
        'text': {
            'tpl': "<a href='/del?nid={nid}'>删除</a>",
            'kwargs': {'nid': '@id'}
        },
        'attrs':{'k1':'v1','k2':'@id'}
    },
]

search_config = [
    {'name': 'cabinet_num', 'text': '机柜号', 'search_type': 'input'},
    {'name': 'device_type_id', 'text': '资产类型', 'search_type': 'select', 'global_name': 'device_type_choices'},
    {'name': 'device_status_id', 'text': '资产状态', 'search_type': 'select', 'global_name': 'device_status_choices'},
]