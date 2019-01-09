from http import cookiejar

import scrapy
from pip._vendor import requests
from selenium import webdriver
import os
from scrapy.selector import Selector

print(os.path.dirname(os.path.abspath(__file__)))



#
# try:
#     browser.execute_script("document.getElementsByClassName('SignFlow-account')[0].getElementsByClassName('Input')[0].value=1840475605;")
# except:
#     pass
# try:
#     browser.execute_script("document.getElementsByClassName('SignFlow-password')[0].getElementsByClassName('Input')[0].value=5178019q.;")
# except:
#     pass
# browser.find_element_by_css_selector('.Login-options button').click()


session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename='zhihu_cookies.txt')
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
'Origin':'https://www.zhihu.com',
'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
'Host':'www.zhihu.com',
'Referer':'https://www.zhihu.com/'

}


def login():
    browser = webdriver.Chrome(executable_path=os.path.dirname(os.path.abspath(__file__)) + "/chromedriver.exe")

    browser.get(
        "https://www.zhihu.com/signup")
    browser.find_element_by_css_selector('.SignContainer-switch span').click()
    # 直接使用该方法已被禁用，改用操作
    browser.find_element_by_css_selector('.SignFlow-account .Input').send_keys("18404975605")
    browser.find_element_by_css_selector('.SignFlow-password .Input').send_keys("5178019q.")
    browser.find_element_by_css_selector('Button.SignFlow-submitButton').click()
    selector = Selector(text=browser.page_source)
    import time
    time.sleep(10)
    cookies=browser.get_cookies()
    print(cookies)
    cookie_dict={}

    import pickle

    for cookie in cookies:
        f=open('H:\python_work_space\project\ArticleSpider/tools\selenium_spicer.py'+cookie['name']+'.zhihu','wb')
        pickle.dump(cookie,f)
        f.close()
        cookie_dict[cookie['name']]=cookie['value']
    browser.close()
    return [scrapy.Request(url='https://www.zhihu.com/',dont_filter=True,cookies=cookie_dict)]
login()
