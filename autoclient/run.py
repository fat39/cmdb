# -*- coding:utf-8 -*-

#######################Agent，每一台设备一份######################
#
# import subprocess
#
# v = subprocess.getoutput("ipconfig")
# value1 = v[20:30]
#
# v2 = subprocess.getoutput("dir")
# value2 = v2[0:5]
#
# url = "http://127.0.0.1:8000/asset.html"
# import requests
#
# response = requests.post(url,data={"k1":value1,"l2":value2})
# print(response.text)


import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="1.1.1.39",port=22,username="root",password="toor")

stdin,stdout,stderr = ssh.exec_command("ls")

result = stdout.read()[0:10]
ssh.close()



url = "http://127.0.0.1:8000/asset.html"
import requests

response = requests.post(url,data={"result":result,})
print(response.text)
