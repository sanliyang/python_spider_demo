"""
爬取美女网

- requests
- bs4
- csv 存储
- 扩展 协程 asyncio
"""
import time

import requests
from bs4 import BeautifulSoup, Tag

from utils.header import get_ua

headers = {
    'User-Agent': get_ua()
}
page = 2
url = 'http://www.meinv.hk/?cat=28'

def get(url):
    resp = requests.get(url, headers= headers)

    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        parse(resp.text)

def parse(html):
    root = BeautifulSoup(html, 'lxml')
    content_boxs = root.select('.content-box')
    for content_box in content_boxs:
        item = {}
        img: Tag = content_box.find('img')
        item['name'] = img.attrs.get('alt')
        item['cover'] = img.attrs.get('src')
        info = content_box.select('.posts-text')[0].string
        try:
            item['title'] = info.split('-')[1]
        except:
            item['title'] = info

        # resp = requests.get(item['cover'], headers=headers)
        # # resp.encoding = 'utf-8'
        # with open(f'{item["name"]}_{item["title"]}.png', 'wb') as f:
        #     f.write(resp.text.encode())
        itempipeline(item)
    # 加载下一页
    post('http://www.meinv.hk/wp-admin/admin-ajax.php')
def post(url):
    print('----下一页-----', url)
    time.sleep(2)
    global page
    resp = requests.post(url, data= {
        "total": 27,
        "action": "fa_load_postlist",
        "paged": page,
        "category": 28,
        "wowDelay": "0.3s"
    }, headers = headers)

    if resp.status_code == 200:
        ret = resp.json()
        page += 1
        parse(ret['postlist'])

def itempipeline(item):
    print(item)

if __name__ == '__main__':
    get(url)