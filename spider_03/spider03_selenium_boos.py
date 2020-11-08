import requests

from selenium.webdriver import Chrome

from utils.header import get_ua

url = 'https://www.zhipin.com/'

headers = {
    'User-Agent': get_ua()
}

def get_allcity():
    base_view = requests.get(url, headers=headers)
    print(base_view.text)


def get_cityjob():
    pass

if __name__ == '__main__':
    get_allcity()