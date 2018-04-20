# -*- coding:utf-8 -*-

from repository import models


class Memory(object):
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()


    def process(self,server_info,server_obj,compare_new_old):
        memory_info = server_info["memory"]
        if not memory_info["status"]:
            models.ErrorLog.objects.create(content=memory_info["data"], asset_obj=server_obj.asset,
                                           title="【%s】内存采集错误信息" % (server_obj.hostname), )

        new_memory_dict = memory_info['data']  # 客户端传来的相关数据
        old_memory_list = models.Memory.objects.filter(server_obj=server_obj)  # 数据库中的数据obj列表
        new_slot_list = list(new_memory_dict.keys())  # 客户端传来的所有slot

        old_slot_list = []
        for item in old_memory_list:
            old_slot_list.append(item.slot)

        # 交集：更新【5，】
        # update_list = set(new_slot_list).intersection(old_slot_list)
        # # 差集：创建【3，】
        # create_list = set(new_slot_list).difference(old_slot_list)
        # # 差集：删除【4，】
        # del_list = set(old_slot_list).difference(new_slot_list)
        update_list,create_list,del_list = compare_new_old(new_slot_list,old_slot_list)

        # 删除【4，】
        models.Memory.objects.filter(server_obj=server_obj,slot__in=del_list).delete()
        if del_list:
            content = "删除内存%s" % ("/".join(del_list))
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content=content,)

        # 创建【3，】
        record_list = []
        create_obj_list = []
        for slot in create_list:
            memory_dict = new_memory_dict[slot]
            memory_dict["server_obj"] = server_obj
            create_obj_list.append(models.Memory(**memory_dict))
            temp = "新增内存：位置{slot}，序列号{sn}，容量{capacity}，型号{model},速率{speed},制造商{manufacturer}".format(**memory_dict)
            record_list.append(temp)

        models.Memory.objects.bulk_create(create_obj_list)
        if record_list:
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=";".join(record_list), )


        # 交集：更新【5，】
        record_list = []
        row_map = {'capacity': "容量", 'slot': '槽位', 'model': '型号', 'speed': '速率', 'manufacturer': '制造商', 'sn': '序列号'}
        for slot in update_list:
            new_memory_row = new_memory_dict[slot]
            # {'capacity': 1024, 'slot': 'DIMM #0', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}
            old_memory_row = models.Memory.objects.filter(server_obj=server_obj,slot=slot).first()
            for k,v in new_memory_row.items():
                if hasattr(old_memory_row,k):
                    value = getattr(old_memory_row,k)
                    if v != value:
                        setattr(old_memory_row,k,v)
                        record_list.append("资产%s，%s由%s变更为%s" % (slot, row_map[k], value, v))
            old_memory_row.save()

        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content=content)






