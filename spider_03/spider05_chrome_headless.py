"""
配置chrome的无头选项
爬去百度贴吧-Python
"""
import time

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')      # 配置无头浏览器
options.add_argument('--disable-gpu')   # 停止浏览器的GPU
# options.binary_location('/usr/bin/chromedriver')         # 驱动程序所在路径

def parse_data(flag = False):
    # 向下滚动1000像素
    js = 'var a = document.documentElement.scrollTop=1000;'
    chrome.execute_script(js)
    # 查找搜索结果
    posts = chrome.find_elements(By.CLASS_NAME, 's_post')
    if flag:
        posts = posts[1:]
    for post in posts:
        a = post.find_element(By.XPATH, './span[1]/a')
        url = a.get_attribute('href')
        title = a.text
        print(url, title)
    time.sleep(1)
    # 查找下一页的标签
    # 网页的大于号 > 一般使用 &gt;
    chrome.find_element(By.LINK_TEXT, '下一页>').click()
    parse_data()

if __name__ == '__main__':

    chrome = Chrome(options=options)

    chrome.get('https://tieba.baidu.com/index.html?traceid=')

    # 查找搜索框元素, 填入Python
    chrome.find_element_by_id('wd1').send_keys('Python')

    #点击搜索按钮
    chrome.find_element(By.CLASS_NAME, 'j_search_post').click()

    time.sleep(1)
    # 解析数据
    parse_data(True)  # True 第一次对搜索的数据去除第一项（user 信息）

    # 截取窗口的屏幕， 保存图片

    chrome.save_screenshot('tieba.png')

    chrome.quit()   #  退出程序

    # chrome.close() # 　关闭当前页签