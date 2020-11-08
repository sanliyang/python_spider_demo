import time
import re, json

import requests
from selenium.webdriver import Chrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions

from utils.header import get_ua

headers = {
    'User-Agent': get_ua()
}
url = 'https://www.zhaopin.com/citymap'
path = '/usr/bin/chromedriver'
chrome = Chrome(executable_path=path)


def get_allcitys():
    resp = requests.get(url=url, headers=headers)
    if resp.status_code == 200:
        html = resp.text
        s = re.search(r'<script>__INITIAL_STATE__=(.*?)</script>', html)
        json_data = s.groups()[0]
        data = json.loads(json_data)
        cityMapList = data['cityList']['cityMapList']
        for letter, citys in cityMapList.items():
            print(f'-------{letter}-------')
            for city in citys:
                """
                {
                    "name": "鞍山",
                    "url": "//www.zhaopin.com/anshan/",
                    "code": "601",
                    "pinyin": "anshan"
			    }, 
                """
                yield city

def get_city_jobs(url):
    print(url)
    chrome.get(url)    # 打开城市信息
    # 查找警告信息的button
    # btn = chrome.find_element_by_css_selector('.risk-warning__content>button')
    # btn.click()
    time.sleep(3)
    input_search: WebElement = chrome.find_element_by_class_name('zp-search__input')
    input_search.send_keys('python')
    # time.sleep(3)
    chrome.find_element_by_class_name('zp-search__btn--blue').click()

    # 当浏览器打开第二个窗口
    w2 = chrome.window_handles[1]
    chrome.switch_to.window(w2)
    time.sleep(5)
    # 页面滚动
    js_to = 'var q = window.document.documentElement.scrollTop=5000'
    chrome.execute_script(js_to)
    time.sleep(0.2)
    print('aaaa')

    try:
        chrome.find_element_by_class_name('a-button a-dialog__close').click()
    except:
        pass
    ui.WebDriverWait(chrome, 60).until(
        expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME,'contentpile'))
    )
    # 判断查询的结果是否存在
    nocontent = chrome.find_element_by_class_name('contentpile')
    if not nocontent:
        print('当前城市未查找到python岗位')
    # 等待 class_name 为 "contentpile" 的div元素的出现

def get_city_jobs2(url):
    chrome.get(url)
    # input_search: WebElement = chrome.find_element_by_css_selector('.search-box__input')
    # input_search.send_keys('python')
    # # time.sleep(3)
    # chrome.find_element_by_class_name('search-box__button').click()
    # 页面滚动
    js_to = 'var q = window.document.documentElement.scrollTop=50000'
    chrome.execute_script(js_to)
    time.sleep(0.2)
    try:
        chrome.find_element_by_class_name('a-button a-dialog__close').click()
    except:
        pass
    ui.WebDriverWait(chrome, 60).until(
        expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME, 'contentpile'))
    )
    # 判断查询的结果是否存在
    nocontent = chrome.find_element_by_class_name('contentpile')
    if not nocontent:
        print('当前城市未查找到python岗位')

if __name__ == '__main__':
    for city in get_allcitys():
        # 保存city 城市信息
        # 请求城市下的所有的Pyhton岗位
        get_city_jobs('https:' + city['url'])
        # print(city['code'])
        # get_city_jobs2(f'https://sou.zhaopin.com/?jl={city["code"]}&kw=python&kt=3')
        time.sleep(30)