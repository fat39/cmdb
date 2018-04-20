import requests

# ################静态令牌 #######################
# key = "adsfasdfzxcvzw241wdsaddsfsdf"
# # response = requests.get("http://127.0.0.1:8000/api/asset.html",headers={"openkey":key})
# response = requests.get("http://127.0.0.1:8000/api/asset.html")
# print(response.text)


# ################ 改良：动态令牌 #######################
# import requests
# import time
# import hashlib
#
# ctime = time.time()
# key = "adsfasdfzxcvzw241wdsaddsfsdf"
# new_key = "%s|%s" % (key,ctime,)
#
# m = hashlib.md5()
# m.update(bytes(new_key,encoding="utf-8"))
# md5_key = m.hexdigest()  # key进行hash
#
# new_time_key = "%s|%s" % (md5_key,ctime,)
#
# response = requests.get("http://127.0.0.1:8000/api/asset.html",headers={"openkey":new_time_key})
# print(response.text)


# from Crypto.Cipher import AES
# pip install pycrypto

# data = "要加密加密加密"
# ba_data = bytearray(data,encoding="utf-8")
# v1 = len(ba_data)
# print(v1)
# v2 = v1 % 16
# v3 = 16 - v2
#
# for i in range(11):
#     ba_data.append(32)

# import requests
#
# key = "adsfasdfzxcvzw241wdsaddsfsdf"
# response = requests.get("http://127.0.0.1:9001/api_check.html",headers={"openkey":key})
# print(response.text)


############################### 加密 ##############################


from Crypto.Cipher import AES


def encrypt(message):
    key = b'dfdsdfsasdfdsdfs'  # key必须是16的整数倍
    cipher = AES.new(key, AES.MODE_CBC, key)  # 创建对象
    ----------------------------------------------
    # 先转成字节,把数据拼够16字节的整数倍
    ba_data = bytearray(message, encoding='utf-8')  # 把数据转成bytearray(byte的数组),bytearray只能追加数字,默认把数字转成字节
    v1 = len(ba_data)
    v2 = v1 % 16
    if v2 == 0:
        v3 = 16
    else:
        v3 = 16 - v2  # v3是追加的长度
    for i in range(v3):
        ba_data.append(v3)  # bytearray只能追加数字,默认把数字转成字节
    final_data = ba_data.decode('utf-8')
    ----------------------------------------------
    msg = cipher.encrypt(final_data)  # 要加密的字符串，必须是16个字节或16个字节的倍数,加密后是byte格式
    return msg


############################### 解密 ##############################
def decrypt(msg):
    key = b'dfdsdfsasdfdsdfs'
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(msg)  # 把加密后的字节解密成不加密的字节
    data = result[0:-result[-1]]
    return str(data, encoding='utf-8')