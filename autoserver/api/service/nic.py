# -*- coding:utf-8 -*-

from repository import models


class NIC(object):
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()


    def process(self,server_info,server_obj,compare_new_old):
        nic_info = server_info["nic"]
        if not nic_info["status"]:
            models.ErrorLog.objects.create(content=nic_info["data"], asset_obj=server_obj.asset,
                                           title="【%s】网卡采集错误信息" % (server_obj.hostname), )

        new_nic_dict = nic_info['data']  # 客户端传来的相关数据
        old_nic_list = models.NIC.objects.filter(server_obj=server_obj)  # 数据库中的数据obj列表
        new_slot_list = list(new_nic_dict.keys())  # 客户端传来的所有slot

        old_slot_list = []
        for item in old_nic_list:
            old_slot_list.append(item.name)


        update_list,create_list,del_list = compare_new_old(new_slot_list,old_slot_list)

        # 删除【4，】
        models.NIC.objects.filter(server_obj=server_obj,name__in=del_list).delete()
        if del_list:
            content = "删除网卡%s" % ("/".join(del_list))
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content=content,)

        # 创建【3，】
        record_list = []
        create_obj_list = []
        for slot in create_list:
            nic_dict = new_nic_dict[slot]
            nic_dict["server_obj"] = server_obj
            nic_dict["name"] = slot
            create_obj_list.append(models.NIC(**nic_dict))
            temp = "新增网卡：名称：{name},网卡mac地址{hwaddr}，ip地址{ipaddrs}，掩码{netmask}，是否启动{up}".format(**nic_dict)
            record_list.append(temp)

        models.NIC.objects.bulk_create(create_obj_list)
        if record_list:
            models.AssetRecord.objects.create(asset_obj=server_obj.asset, content=";".join(record_list), )


        # 交集：更新【5，】
        record_list = []
        row_map = {'name': "名称", 'hwaddr': 'mac地址', 'ipaddrs': 'ip地址', 'netmask': '掩码', 'up': '是否启动'}
        for slot in update_list:
            new_nic_row = new_nic_dict[slot]
            # {'capacity': 1024, 'slot': 'DIMM #0', 'model': 'DRAM', 'speed': '667 MHz', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}
            old_nic_row = models.NIC.objects.filter(server_obj=server_obj,name=slot).first()
            for k,v in new_nic_row.items():
                if hasattr(old_nic_row,k):
                    value = getattr(old_nic_row,k)
                    if v != value:
                        setattr(old_nic_row,k,v)
                        record_list.append("资产%s，%s由%s变更为%s" % (slot, row_map[k], value, v))
            old_nic_row.save()

        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content=content)






