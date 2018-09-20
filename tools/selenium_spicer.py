from selenium import webdriver

browser = webdriver.Chrome(executable_path="E:/workSpace/py_work_space/driver/chromedriver.exe")
browser.get(
    "https://www.baidu.com/s?tn=95148558_hao_pg&isource=infinity&iname=baidu&itype=web&ie=utf-8&wd=%E6%85%95%E8%AF%BE%E7%BD%91")
print(browser.page_source)
