"""
基于进程+ 线程实现多任务爬虫程序
"""
import time
import uuid
from queue import Queue as TQueue
from multiprocessing import Queue,  Process
from threading import Thread

import requests
from requests import Response
from lxml import etree

from utils.header import get_ua

headers = {
    'User-Agent': get_ua()
}

class DownloadThread(Thread):
    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue = task_queue       # 线程队列
        self.result_queue: Queue = result_queue   # 进程的队列
    # 开始下载
    def run(self):
        while True:
            try:
                url = self.task_queue.get(timeout=10)
                content = self.get(url)
                self.result_queue.put((url, content))
            except:
                break

    def get(self, url):
        print('开始下载',url)
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            resp.encoding = 'utf-8'
        print(url, '下载完成')
        return resp.text



class DownLoadProcess(Process):
    """下载进程"""
    def __init__(self, url_q, html_q):
        self.url_q: Queue = url_q
        self.html_q = html_q

        super().__init__()
        # 用于进程内部多个线程之间的通信队列
        self.task_queue = TQueue()

    def run(self):
        # 启动子线程下载任务
        ts = [DownloadThread(self.task_queue, self.html_q)
              for i in range(2)]
        for t in ts:
            t.start()

        while True:
            try:
                url = self.url_q.get(timeout=30)
                self.task_queue.put(url)
            except:
                break
        for t in ts:
            t.join()
        print('下载进程over')

class ParseThread(Thread):
    def __init__(self, html, url_q, parent_url):
        self.html = html
        self.url_q = url_q
        self.parent_url = parent_url
        super(ParseThread, self).__init__()

    def run(self):
        root = etree.HTML(self.html)
        imgs = root.xpath('//div[contains(@class, "picblock")]//img')
        item = {}
        for img in imgs:
            item['id'] = uuid.uuid4().hex
            item['name'] = img.xpath('./@alt')[0]
            try:
                item['cover'] = img.xpath('./@src2')[0]
            except:
                item['cover'] = img.xpath('./@src')[0]
            # 将item 数据写入到 ES 索引库中
        print(item)
        # 获取下一页链接
        next_url = self.parent_url + root.xpath('//a[@class="nextpage]/@href')[0]
        self.url_q.put(next_url)  # 将新的下载任务添加到下载队列中

class ParaseProcess(Process):
    # 解析进程
    def __init__(self, url_q, html_q):
        self.url_q = url_q
        self.html_q = html_q
        super(ParaseProcess, self).__init__()

    def run(self):
        while True:
            try:
                # 读取解析的任务
                url, html = self.html_q.get(timeout=60)
                print(f'开始解析{url}')
                parent_url = url[:url.rindex('/') + 1]
                ParseThread(html, self.url_q, parent_url).start()
            except:
                break
        print('解析进程Over')

if __name__ == '__main__':
    task1 = Queue()   # 下载任务队列
    task2 = Queue()   # 解析任务队列

    # 起始爬虫任务
    task1.put('http://sc.chinaz.com/tupian/shuaigetupian.html')       # url

    p1 = DownLoadProcess(task1, task2)
    p2 = ParaseProcess(task1, task2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print('-----over-----')