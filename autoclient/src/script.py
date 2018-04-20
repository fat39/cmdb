# -*- coding:utf-8 -*-
from lib.conf.config import settings
from .client import Agent,SSHSALT

def run():
    if settings.MODE == "AGENT":
        obj = Agent()
    else:
        obj = SSHSALT()
    obj.execute()
