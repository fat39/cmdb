# -*- coding:utf-8 -*-
from lib.conf.config import settings
from .client import Agent,SSHSALT

def run():
    if settings.MODE == "AGENT":
        obj = Agent()
    else:
        obj = SSHSALT()
    obj.execute()


# 入口
# 在script总入口使用client的execute
# client使用插件类获取server_info
# 插件类工作流程：
    # 导入所有插件
    # 插件运行process方法，实则执行cmd方法
        # 插件获取content
        # parse解析content，获取结果
# client发送到api