# -*- coding:utf-8 -*-
import requests
import subprocess

result = subprocess.getoutput("ifconfig")


url = "http://127.0.0.1:8000/asset.html"
# url = "http://1.1.1.1:8000/asset.html"  # linux上配置
response = requests.post(url,data={"check":result})
print(response.text)

# 在Django服务器配置绑定ip1.1.1.1，设置ALLOWED_HOSTS = ["1.1.1.1",]