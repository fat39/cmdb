import json
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from repository import models
from django.conf import settings
import time
from api.service import PluginManager

api_key_record = {}
def API_check(func):
    def wrapper(request,*args,**kwarg):
        if request.method == "GET":
            import hashlib
            # ####################API认证##################
            client_md5_time_key = request.META.get("HTTP_OPENKEY")
            client_md5_key, client_ctime = client_md5_time_key.split("|")
            client_ctime = float(client_ctime)
            server_time = time.time()
            # 第一关
            if server_time - client_ctime > 10:
                return HttpResponse("【第一关】时间有点长")

            # 第二关
            tmp = "%s|%s" % (settings.AUTH_KEY, str(client_ctime))
            m = hashlib.md5()
            m.update(bytes(tmp, encoding="utf-8"))
            server_md5_key = m.hexdigest()
            if server_md5_key != client_md5_key:
                return HttpResponse("【第二关】规则不正确，验证码错误")

            for k in list(api_key_record.keys()):
                v = api_key_record[k]
                if server_time > v:
                    api_key_record.pop(k)

            # 第三关
            if client_md5_time_key in api_key_record:
                return HttpResponse("【第三关】有人已经来过了")
            else:
                api_key_record[client_md5_time_key] = client_ctime + 10

        # ####################API认证##################
        ret = func(request,*args,**kwarg)
        return ret
    return wrapper


@API_check
def asset(request):
    # if request.method == "GET":
        # import hashlib
        #
        # # ####################API认证##################
        # client_md5_time_key = request.META.get("HTTP_OPENKEY")
        # client_md5_key,client_ctime = client_md5_time_key.split("|")
        # client_ctime = float(client_ctime)
        # server_time = time.time()
        # # 第一关
        # if server_time - client_ctime > 10:
        #     return HttpResponse("【第一关】时间有点长")
        #
        # # 第二关
        # tmp = "%s|%s" % (settings.AUTH_KEY,str(client_ctime))
        # m = hashlib.md5()
        # m.update(bytes(tmp,encoding="utf-8"))
        # server_md5_key = m.hexdigest()
        # if server_md5_key != client_md5_key:
        #     return HttpResponse("【第二关】规则不正确，验证码错误")
        #
        # for k in list(api_key_record.keys()):
        #     v = api_key_record[k]
        #     if server_time > v:
        #         api_key_record.pop(k)
        #
        #
        # # 第三关
        # if client_md5_time_key in api_key_record:
        #     return HttpResponse("【第三关】有人已经来过了")
        # else:
        #     api_key_record[client_md5_time_key] = client_ctime + 10



    # ####################API认证##################

    if request.method == "POST":


        # 新资产信息
        server_info = json.loads(request.body.decode("utf-8"))


        hostname = server_info["basic"]["data"]["hostname"]
        # 老资产信息
        server_obj = models.Server.objects.filter(hostname=hostname).first()
        if not server_obj:
            return HttpResponse("当前主机名在资产中未录入")
        # asset_obj = server_obj.asset

        for k,v in server_info.items():
            print(k,v)

        PluginManager(server_info,server_obj).exec_plugin()
        # # ############# 处理硬盘信息 #############
        # if not server_info["disk"]["status"]:
        #     models.ErrorLog.objects.create(content=server_info["disk"]["data"],asset_obj=server_obj.asset,title="【%s】硬盘采集错误信息" % (hostname),)
        #
        # new_disk_dict = server_info['disk']['data']
        # """
        # {
        #     5: {'slot':5,capacity:476...}
        #     3: {'slot':3,capacity:476...}
        # }
        # """
        # old_disk_list = models.Disk.objects.filter(server_obj=server_obj)
        # """
        # [
        #     Disk('slot':5,capacity:476...)
        #     Disk('slot':4,capacity:476...)
        # ]
        # """
        # # 交集：5, 创建：3,删除4;
        # new_slot_list = list(new_disk_dict.keys())
        #
        # old_slot_list = []
        # for item in old_disk_list:
        #     old_slot_list.append(item.slot)
        #
        # # 交集：更新【5，】
        # update_list = set(new_slot_list).intersection(old_slot_list)
        # # 差集：创建【3，】
        # create_list = set(new_slot_list).difference(old_slot_list)
        # # 差集：删除【4，】
        # del_list = set(old_slot_list).difference(new_slot_list)
        #
        #
        #
        # # 删除【4，】
        # models.Disk.objects.filter(server_obj=server_obj,slot__in=del_list).delete()
        # # 记录日志
        # if del_list:
        #     models.AssetRecord.objects.create(asset_obj=server_obj.asset,content="移除硬盘：%s" % ("/".join(del_list)))
        #
        #
        # # 创建【3，】
        # record_list = []
        # create_obj_list = []
        # for slot in create_list:
        #     disk_dict = new_disk_dict[slot]
        #     disk_dict["server_obj"] = server_obj
        #     create_obj_list.append(models.Disk(**disk_dict))
        #     temp = "新增硬盘：位置{slot}，容量{capacity}，型号{model},类型{pd_type}".format(**disk_dict)
        #     record_list.append(temp)
        # models.Disk.objects.bulk_create(create_obj_list)
        #
        # if record_list:
        #     content = ";".join(record_list)
        #     models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)
        #
        #
        # # 更新【5，】
        # record_list = []
        # row_map = {"capacity":"容量","pd_type":"类型","model":"型号"}
        # for slot in update_list:
        #     new_disk_row = new_disk_dict[slot]
        #     old_disk_row = models.Disk.objects.filter(server_obj=server_obj,slot=slot).first()
        #     for k,v in new_disk_row.items():
        #         value = getattr(old_disk_row,k)
        #         if v != value:
        #             record_list.append("资产%s，%s由%s变更为%s" % (slot,row_map[k],value,v))
        #             setattr(old_disk_row,k,v)
        #     old_disk_row.save()
        #
        # if record_list:
        #     content = ";".join(record_list)
        #     models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)




        # 资产表中以前资产信息
        # server_obj可以找到服务器的基本信息（单条）
        # server_obj.disk.all()


        # 处理：
        """
        1. 根据新资产和原资产进行比较：新["5","1"]      老["4","5","6"]
        2. 增加: [1,]   更新：[5,]    删除：[4,6]
        3. 增加：
                server_info中根据[1,],找到资产详细：入库
           删除：
                数据库中找当前服务器的硬盘：[4,6]

           更新：[5,]
                disk_list = [obj,obj,obj]

                {
                    'data': {
                        '5': {'slot': '5', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'},
                        '3': {'slot': '3', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAF912433K     Samsung SSD 840 PRO Series              DXM06B0Q'},
                        '4': {'slot': '4', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series              DXM05B0Q'},
                        '0': {'slot': '0', 'capacity': '279.396', 'pd_type': 'SAS', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'},
                        '2': {'slot': '2', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'},
                        '1': {'slot': '1', 'capacity': '279.396', 'pd_type': 'SAS', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'}
                    },

                    'status': True
                }

                log_list = []

                dict_info = {'slot': '5', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'},
                obj
                    if obj.capacity != dict_info['capacity']:
                        log_list.append('硬盘容量由%s变更为%s' %s(obj.capacity,dict_info['capacity'])
                        obj.capacity = dict_info['capacity']
                    ...
                obj.save()

                models.xxx.object.create(detail=''.join(log_list))

        """



    return HttpResponse("...")


# http://127.0.0.1:8000/api/servers.html GET:获取服务器列表
# http://127.0.0.1:8000/api/servers.html POST:创建服务器
# http://127.0.0.1:8000/api/servers/1.html GET:获取单条信息
# http://127.0.0.1:8000/api/servers/1.html DELETE：删除单条信息
# http://127.0.0.1:8000/api/servers/1.html PUT：更新

def servers(request):
    if request.method == "GET":
        v = models.Server.objects.values("id","hostname")
        server_list = list(v)
        # return JsonResponse({"a":1,"b":2})  # 默认只能发字典
        return JsonResponse(server_list,safe=False)  # safe=False时才能发list
    elif request.method == "POST":
        return JsonResponse(status=201)

def servers_detail(request,nid):
    if request.method == "GET":
        obj = models.Server.objects.filter(id=nid).first()
        return HttpResponse("...")
    elif request.method == "DELETE":
        obj = models.Server.objects.filter(id=nid).delete()
        return HttpResponse
    elif request.mothod == "PUT":
        # request.body
        models.Server.objects.filter(id=nid).update()


##########################################################

from rest_framework import serializers
class ServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Server
        fields = ("id","asset__cabinet_num","hostname","sn")  # fields = "__all__"
        # exclude = ('ug',)
        depth = 1  # 0<=depth<=10



from rest_framework import viewsets
class ServerViewSet(viewsets.ModelViewSet):
    queryset = models.Server.objects.all().order_by("-id")
    serializer_class = ServerSerializer