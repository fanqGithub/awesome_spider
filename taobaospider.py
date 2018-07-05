import re

from selenium import webdriver
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

# driver = webdriver.Chrome()
# driver.get("http://www.baidu.com")
# driver.find_element_by_id('kw').send_keys('selenium')
# driver.find_element_by_id('su').click()

# 本节学习的是使用爬虫利器：selenium + chromedriver进行网站信息的爬取，对于返回的信息在element 中的信息应该采用的方式。

browser = webdriver.Chrome()
wait =WebDriverWait(browser,10)

def search():
    # try:
    browser.get('https://www.taobao.com/')
    input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
    submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
    input.send_keys('手机')
    submit.click()
    parse_element()
        # total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        # return total.text
    # except TimeoutError:
    #     return search()

def next_page(pageindex):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(pageindex)
        submit.click()
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(pageindex)))
        parse_element()
    except TimeoutError:
        next_page(pageindex)

def parse_element():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)


def gospider():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2, total + 1):
            next_page(i)
    except Exception:
    finally:
        browser.close()


if __name__ == '__main__':
    search()