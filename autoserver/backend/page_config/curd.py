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
        'attrs':{'k1':'v1','k2':'@hostname'}

    },
    {
        'q': 'hostname',
        'title': '主机名',
        'display': True,
        'text': {
            'tpl': "{n1}",
            'kwargs': {'n1': '@hostname'}
        },
        'attrs':{'edit-enable':'true','origin':'@hostname','name':'hostname'}

    },
     {
        'q': 'sn',
        'title': 'SN号',
        'display': True,
        'text': {
            'tpl': "{n1}",
            'kwargs': {'n1': '@sn'}
        },
        'attrs':{}

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
        'attrs':{'k1':'v1','k2':'@hostname'}
    },
]

search_config =  [
    {'name': 'hostname__contains', 'text': '主机名', 'search_type': 'input'},
    {'name': 'sn__contains', 'text': 'SN号', 'search_type': 'input'},
]