# -*- coding:utf-8 -*-
from repository import models


class Disk(object):
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def process(self,server_info,server_obj,compare_new_old):
        disk_info = server_info["disk"]
        if not disk_info["status"]:
            models.ErrorLog.objects.create(content=disk_info["data"], asset_obj=server_obj.asset,
                                           title="【%s】硬盘采集错误信息" % (server_obj.hostname), )

        new_disk_dict = disk_info['data']  # 客户端传来的相关数据
        old_disk_list = models.Disk.objects.filter(server_obj=server_obj)  # 数据库中的数据obj列表
        new_slot_list = list(new_disk_dict.keys())  # 客户端传来的所有slot

        old_slot_list = []
        for item in old_disk_list:
            old_slot_list.append(item.slot)

        # 交集：更新【5，】
        # update_list = set(new_slot_list).intersection(old_slot_list)
        # # 差集：创建【3，】
        # create_list = set(new_slot_list).difference(old_slot_list)
        # # 差集：删除【4，】
        # del_list = set(old_slot_list).difference(new_slot_list)
        update_list, create_list, del_list = compare_new_old(new_slot_list,old_slot_list)


        # 删除【4，】
        models.Disk.objects.filter(server_obj=server_obj, slot__in=del_list).delete()  # 删除在del_list的
        # 记录日志
        if del_list:
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content="移除硬盘：%s" % ("/".join(del_list)))


        # 创建【3，】
        record_list = []
        create_obj_list = []
        for slot in create_list:
            disk_dict = new_disk_dict[slot]
            disk_dict["server_obj"] = server_obj
            create_obj_list.append(models.Disk(**disk_dict))
            temp = "新增硬盘：位置{slot}，容量{capacity}，型号{model},类型{pd_type}".format(**disk_dict)
            record_list.append(temp)
        models.Disk.objects.bulk_create(create_obj_list)
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)


        # 更新【5，】
        record_list = []
        row_map = {"capacity":"容量","pd_type":"类型","model":"型号"}
        for slot in update_list:
            new_disk_row = new_disk_dict[slot]
            old_disk_row = models.Disk.objects.filter(server_obj=server_obj,slot=slot).first()
            for k,v in new_disk_row.items():
                value = getattr(old_disk_row,k)
                if v != value:
                    record_list.append("资产%s，%s由%s变更为%s" % (slot,row_map[k],value,v))
                    setattr(old_disk_row,k,v)
            old_disk_row.save()

        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=content)












