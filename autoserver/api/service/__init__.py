# -*- coding:utf-8 -*-
import importlib
from django.conf import settings


class PluginManager(object):
    def __init__(self,server_info,server_obj):
        self.server_info = server_info
        self.server_obj = server_obj


    def exec_plugin(self):
        for name,p_path in settings.PLUGINS_DICT.items():
            module_path,class_name = p_path.rsplit(".",1)
            m = importlib.import_module(module_path)
            if hasattr(m,class_name):
                cls = getattr(m,class_name)
                if hasattr(cls,'initial'):
                    obj = cls.initial()
                else:
                    obj = cls()
                obj.process(self.server_info,self.server_obj,self.compare_new_old)



    def compare_new_old(self,new_slot_list,old_slot_list):
        # 交集：更新【5，】
        update_list = set(new_slot_list).intersection(old_slot_list)
        # 差集：创建【3，】
        create_list = set(new_slot_list).difference(old_slot_list)
        # 差集：删除【4，】
        del_list = set(old_slot_list).difference(new_slot_list)

        return update_list,create_list,del_list