# -*- coding:utf-8 -*-
import requests
from scrapy.selector import Selector

url = "http://www.taiyingshi.com/dm/tw938.html"  # 5
url = "http://www.taiyingshi.com/dm/tw1232.html"  # 6
url = "http://www.taiyingshi.com/dm/tw2282.html"  # 1
htm = requests.get(url)

sel = Selector(response=htm)

thunder_list = sel.xpath("//a[starts-with(@href, 'thunder')]/@href").extract()

for link in thunder_list:
    print(link)



