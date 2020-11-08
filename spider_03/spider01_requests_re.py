"""
基于正则 re 模块来解析数据
"""
import re
import os

import requests
from requests import Response

from utils.header import get_ua

base_url = 'http://sc.chinaz.com/tupian/'

url = 'http://sc.chinaz.com/tupian/shuaigetupian.html'
if os.path.exists('mn.html'):
    with open('mn.html','r',encoding='utf-8') as f:
        html = f.read()
else:
    resp: Response = requests.get(url, headers = {'User-Agent': get_ua()})
    print(resp.encoding)          # ISO-8859-1   这是国际标准编码
    resp.encoding = 'utf-8'       # 可以修改响应的状态码
    assert resp.status_code == 200
    html = resp.text
    with open('mn.html', 'w') as f:
        f.write(html)
# print(html)
# [\u4e00-\u9fa5]
compile = re.compile(r'<img src2="(.*?)" alt="(.*?)">')
compile2 = re.compile(r'<img alt="(.*?)" src="(.*?)" >')
imgs = compile.findall(html)   # list
if len(imgs) == 0:
    imgs = compile2.findall(html)

print(len(imgs), imgs, sep="\n")

next_url = re.findall(r'<b>25</b></a><a href="(.*?)" class="nextpage">', html, re.S)
# print(next_url)
print(base_url+next_url[0])
