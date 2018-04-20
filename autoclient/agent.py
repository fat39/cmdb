# -*- coding:utf-8 -*-

import subprocess
import requests

cmd = "dir"
result = subprocess.getoutput(cmd)

url = "http://127.0.0.1:8000/asset.html"
response = requests.post(url,data={"result":result})
print(response.text)
