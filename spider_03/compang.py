import os
import re
import time
from csv import DictWriter
from urllib.request import build_opener, HTTPHandler, HTTPCookieProcessor,ProxyHandler,Request
from http.cookiejar import CookieJar
from urllib.parse import urlencode


opener = build_opener(HTTPHandler(),
                      HTTPCookieProcessor(CookieJar()),
                      ProxyHandler(proxies={
                          'http':'http://27.43.188.133:9999',
                          'http':'http://220.249.149.145:9999',
                          'http':'http://27.43.188.123:9999'
                      }))
page = 1

good_url = f'http://jy.ayit.edu.cn/module/milkrounddetail/id-5f893bb2c623474328cd696b/nid-3639/page-{page}'

base_url = 'http://jy.ayit.edu.cn'

import requests
from lxml import etree
from bs4 import BeautifulSoup

from utils.header import get_ua

headers = {
    'User-Agent' : get_ua()
}
def download(good_url):
    print(good_url)
    request = Request(good_url,headers=headers)
    try:
        resp = opener.open(request, timeout=10)
    except:
        resp = requests.get(good_url,headers=headers)
    html = resp.text
    parse(html)

def get(url):
    request = Request(url, headers=headers)
    try:
        resp = opener.open(request, timeout=10)
    except:
        resp = requests.get(url, headers=headers)
    html = resp.text
    get_detail_parse(html)

def parse(html):
    if html:
        root = etree.HTML(html)
        lis = root.xpath('//div[@class="company_content"]/ul[@class="company"]/li')
        print(lis)
        item = {}
        for li in lis:
            lil = li.xpath('./a/@href')[0]
            url = base_url + lil      # 下一页url
            get(url)
        global page
        page += 1
        print(page)
        if page <= 10:
            good_url = f'http://jy.ayit.edu.cn/module/milkrounddetail/id-5f893bb2c623474328cd696b/nid-3639/page-{page}'
            download(good_url)
        else:
            pass

def get_detail_parse(html):
    if html:
        root = etree.HTML(html)
        divs = root.xpath('//*[@id="centerFrame"]/div[2]/div[2]/div')
        for div in divs:
            name = div.xpath('./div[1]/div[2]/div[1]/span[1]/text()')
            zhiweis = div.xpath('./div[3]/div[2]/div')
            item = {}
            item['compang'] = name
            for zhiwei in zhiweis:
                try:
                    item['position'] = zhiwei.xpath('.//span[@class="p-black pp"]/text()')[0]
                except:
                    item['position'] = '未知'
                cc = zhiwei.xpath('.//span[@class="p-black pp"]/text()')[1]
                dd = re.findall(r'([\u4e00-\u9fa5]+)', cc)
                item['dili'] = dd
                try:
                    ee = zhiwei.xpath('.//span[@class="pay"]/text()')[0]
                except:
                    ee = 'no'
                try:
                    ll = zhiwei.xpath('.//span[@class="level"]/text()')[0]
                except:
                    ll = '不限'
                item['pay'] = ee
                item['level'] = ll
                print(item)
                itempipline4csv(item)

has_header = os.path.exists('company1.csv');  # 是否第一个写入 csv的头
header_fileds = ('compang', 'dili', 'position','pay', 'level')
def itempipline4csv(item):
    print(item)
    global has_header
    with open('company1.csv', 'a') as f:
        write = DictWriter(f, header_fileds)
        if not has_header:
            write.writeheader()   # 写入第一行的标题
            has_header = True
        write.writerow(item)


if __name__ == '__main__':
    download(good_url)