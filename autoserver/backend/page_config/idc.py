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
                'text': {},
                'attrs':{}
            },
            {
                'q': 'name',
                'title': '机房名称',
                'display': True,
                'text': {
                    'tpl': "{n1}",
                    'kwargs': {'n1': '@name'}
                },
                'attrs':{'edit-enable':'true','origin':'@name','name':'name'}
            },
            {
                'q': 'floor',
                'title': '楼层',
                'display': True,
                'text': {
                    'tpl': "{n1}",
                    'kwargs': {'n1': '@floor'}
                },
                'attrs':{'edit-enable':'true','origin':'@floor','name':'floor'}
            }
        ]