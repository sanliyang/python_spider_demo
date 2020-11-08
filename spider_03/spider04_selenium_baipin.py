import json
import time

import requests
from selenium.webdriver import Chrome
from urllib.parse import quote
from selenium.webdriver.common.by import By

from selenium.webdriver.support import ui, expected_conditions


def start(city_name):
    url = f'https://zhaopin.baidu.com/?query=&city={quote(city_name)}'
    chrome.get(url)
    query = chrome.find_element_by_css_selector('input[name="query"]')
    query.send_keys("python")

    chrome.find_element_by_css_selector('.search-btn').click()

    time.sleep(0.5)

    chrome.execute_script('var a =  document.documentElement.scrollTop=100000')

    # 等待class 为 listitems 的div标签出现
    ui.WebDriverWait(chrome, 60).until(
        expected_conditions.visibility_of_all_elements_located((
            By.CLASS_NAME, 'listitems'
        )),
        'listitems的div元素没有出现'
    )

    # 连续向下滚动10次
    for i in range(11):
        chrome.execute_script('var a =  document.documentElement.scrollTop=100000')
        time.sleep(1)

    # 获取所有岗位信息
    items = chrome.find_elements(By.CSS_SELECTOR, '.listitem>a')
    items = items[1:] # 第一个a标签是一个广告
    for item in items:
        try:
            #过滤当前的数据是否是广告
            adv = item.find_element(By.CLASS_NAME, 'adbar-item.gap-left-small')
            continue
        except:
            pass
        data = item.find_element(By.TAG_NAME, 'div').get_attribute('data-click')
        # info_url = item.get_attribute('href')    # 岗位的详情链接
        info = json.loads(data)['url']
        title = item.find_element(By.CLASS_NAME, 'title').text
        salary= item.find_element(By.CSS_SELECTOR, '.salaryarea span').text
        print(info, title, salary)

if __name__ == '__main__':
    # chromedriver.exe 驱动程序路径已配置到path环境变量里面
    chrome = Chrome()
    start('郑州')
    time.sleep(5)
    chrome.close()    # 关闭浏览器