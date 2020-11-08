import asyncio

import requests
from bs4 import BeautifulSoup, Tag

from utils.header import get_ua

headers = {
    'User-Agent': get_ua()
}
@asyncio.coroutine
def get(url):
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        resp.encoding = 'utf-8'
        yield from parse(resp.text)

@asyncio.coroutine
def post(url, page=2):
    print('----下一页-----', url, page)
    resp = requests.post(url, data={
        "total": 27,
        "action": "fa_load_postlist",
        "paged": page,
        "category": 28,
        "wowDelay": "0.3s"
    }, headers=headers)

    if resp.status_code == 200:
        ret = resp.json()
        yield from parse(ret['postlist'])
    yield from post(url, page+1)

@asyncio.coroutine
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
        yield from itempipeline(item)

@asyncio.coroutine
def itempipeline(item):
    print(item)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # 起始协程是单个
    # loop.run_until_complete(get(''))
    # 起始多个协程
    loop.run_until_complete(asyncio.wait((
        get('http://www.meinv.hk/?cat=28'),
        post('http://www.meinv.hk/wp-admin/admin-ajax.php')
    )))
    loop.close()