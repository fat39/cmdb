import json
from django.shortcuts import render, HttpResponse
from repository import models
from datetime import datetime
from datetime import date
from django.conf import settings

class JsonCustomEncoder(json.JSONEncoder):

    def default(self, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, value)


def curd(request):
    # v = models.Server.objects.all()
    return render(request, 'curd.html')


def curd_json(request):
    if request.method == 'DELETE':
        id_list = json.loads(str(request.body,encoding='utf-8'))
        # models.Server.objects.filter(id__in=id_list).delete()  # 先注销，防止误操作
        return HttpResponse('....')
    elif request.method == "PUT":
        all_list = json.loads(str(request.body,encoding='utf-8'))
        for item in all_list:
            if item:
                item_id = item.pop("id")
                models.Server.objects.filter(id=item_id).update(**item)
        return HttpResponse('....')
    elif request.method == "POST":
        pass
    elif request.method == 'GET':
        from backend.page_config.curd import table_config,search_config
        values_list = []
        for row in table_config:
            if not row['q']:
                continue
            values_list.append(row['q'])

        # 获取搜索条件
        condition_list = json.loads(request.GET.get("condition"))
        from django.db.models import Q
        con = Q()
        for k,v in condition_list.items():
            q = Q()
            q.connector = "OR"
            for item in v:
                if not item:
                    continue
                q.children.append((k,item))
            con.add(q,"AND")
        print(con)
        server_list = models.Server.objects.filter(con).values(*values_list)

        ret = {
            'server_list': list(server_list),
            'table_config': table_config,
            "search_config":search_config,
        }

        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def asset(request):
    return render(request, 'asset.html')


def asset_json(request):
    if request.method == 'DELETE':
        id_list = json.loads(str(request.body,encoding='utf-8'))
        # models.Asset.objects.filter(id__in=id_list).delete()  # 先注销，防止误操作
        return HttpResponse('...')
    elif request.method == "PUT":
        all_list = json.loads(str(request.body,encoding='utf-8'))
        for row in all_list:
            nid = row.pop('id')
            models.Asset.objects.filter(id=nid).update(**row)
        return HttpResponse('....')
    elif request.method == "POST":
        pass
    elif request.method == 'GET':
        from backend.page_config.asset import table_config,search_config
        values_list = []
        for row in table_config:
            if not row['q']:
                continue
            values_list.append(row['q'])

        # 获取搜索条件
        condition_list = json.loads(request.GET.get("condition"))
        from django.db.models import Q
        con = Q()
        for k,v in condition_list.items():
            q = Q()
            q.connector = "OR"
            for item in v:
                if not item:
                    continue
                q.children.append((k,item))
            con.add(q,"AND")
        server_list = models.Asset.objects.filter(con).values(*values_list)


        # 页码
        current_page = int(request.GET.get("current_page"))
        per_page = settings.PER_PAGE  # 每页显示条目
        all_count = server_list.count()  # 一共多少条目
        page_count = all_count // per_page + 1  # 一共多少页
        start = per_page * (current_page - 1)
        end = per_page * (current_page)
        server_list = server_list[start:end]
        pager = {"page_count":page_count,"current_page":current_page}

        ret = {
            'server_list': list(server_list),
            'table_config': table_config,
            "search_config":search_config,
            'global_dict':{
                'device_type_choices': models.Asset.device_type_choices,
                'device_status_choices': models.Asset.device_status_choices,
                'idc_choices': list(models.IDC.objects.values_list('id','name'))
            },
            "pager":pager,
            # "page_count": page_count,
            # "current_page":current_page,
        }
        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def idc(request):
    return render(request,'idc.html')

def idc_json(request):
    if request.method == 'DELETE':
        id_list = json.loads(str(request.body,encoding='utf-8'))
        # models.IDC.objects.filter(id__in=id_list).delete()  # 先注销，防止误操作
        return HttpResponse('。。。')
    elif request.method == "PUT":
        all_list = json.loads(str(request.body, encoding='utf-8'))
        for item in all_list:
            if item:
                item_id = item.pop("id")
                models.IDC.objects.filter(id=item_id).update(**item)
        return HttpResponse('....')
    elif request.method == 'GET':
        from backend.page_config import idc
        values_list = []
        for row in idc.table_config:
            if not row['q']:
                continue
            values_list.append(row['q'])

        server_list = models.IDC.objects.values(*values_list)

        ret = {
            'server_list': list(server_list),
            'table_config': idc.table_config,
            'global_dict':{}

        }
        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))