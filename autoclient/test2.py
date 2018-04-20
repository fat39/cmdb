# -*- coding:utf-8 -*-
# import requests
# tag = "b2fe21e73cbda63195917727bf57932a|1520241253.8395703"
# response = requests.get(url="http://127.0.0.1:8000/api/asset.html",headers={"openkey":tag})
# print(response.text)

# disk_dict = {"slot":1,"capacity":100,"model":123,"pd_type":1,"test":"test"}
# a = "新增硬盘：位置{slot}，容量{capacity}，型号{model},类型{pd_type}".format(**disk_dict)
# print(a)

import socket

client = socket.socket()
client.connect(("127.0.0.1",9000))
client.send(b"haha")

client.close()