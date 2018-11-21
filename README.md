# cmdb

# client端

## 流程
入口
在script总入口使用client的execute
client使用插件类获取server_info
插件类工作流程：
    导入所有插件
    插件运行process方法，实则执行cmd方法
        插件获取content
        parse解析content，获取结果
client发送到api





## 插件式导入模块
### setting.py
```
PLUGINS_DICT = {
    "basic":"src.plugins.basic.Basic",
    "board":"src.plugins.board.Board",
    "cpu":"src.plugins.cpu.Cpu",
    "disk":"src.plugins.disk.Disk",
    "memory":"src.plugins.memory.Memory",
    "nic":"src.plugins.nic.Nic",
}
```

### __init__.py
```
class PluginManager(object):

    def exec_plugin(self):
        """
        获取所有的插件，并执行获取插件返回值
        :return:
        """
        response = {}
        for k,v in self.plugin_dict.items():
            #  'basic': "src.plugins.basic.Basic",
            ret = {'status':True,'data':None}
            try:
                module_path, class_name = v.rsplit('.', 1)
                m = importlib.import_module(module_path)
                cls = getattr(m,class_name)
                if hasattr(cls,'initial'):
                    obj = cls.initial()  # 钩子
                else:
                    obj = cls()
```
		

# server端
repository  统一数据库
backend  后台管理+前端页面，可与api分离
api  可与backend分离


api认证，time-key-record
client端发送server_info到api，api把数据存入数据库
backend端访问数据，供前端页面使用


api认证
```
def API_check(func):
    def wrapper(request,*args,**kwarg):
        if request.method == "GET":
            import hashlib
            # ####################API认证##################
            client_md5_time_key = request.META.get("HTTP_OPENKEY")
            client_md5_key, client_ctime = client_md5_time_key.split("|")
            client_ctime = float(client_ctime)
            server_time = time.time()
            # 第一关
            if server_time - client_ctime > 10:
                return HttpResponse("【第一关】时间有点长")

            # 第二关
            tmp = "%s|%s" % (settings.AUTH_KEY, str(client_ctime))
            m = hashlib.md5()
            m.update(bytes(tmp, encoding="utf-8"))
            server_md5_key = m.hexdigest()
            if server_md5_key != client_md5_key:
                return HttpResponse("【第二关】规则不正确，验证码错误")

            for k in list(api_key_record.keys()):
                v = api_key_record[k]
                if server_time > v:
                    api_key_record.pop(k)

            # 第三关
            if client_md5_time_key in api_key_record:
                return HttpResponse("【第三关】有人已经来过了")
            else:
                api_key_record[client_md5_time_key] = client_ctime + 10

        # ####################API认证##################
        ret = func(request,*args,**kwarg)
        return ret
    return wrapper
```


## 插件式处理数据，与client端类似，__init__.py
```
class PluginManager(object):
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
```















