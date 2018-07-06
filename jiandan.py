import os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import  By
import requests
from multiprocessing import Pool

browser=webdriver.Chrome()
wait=WebDriverWait(browser,10)

def openJiandan(pageindex):
    url='http://jandan.net/ooxx/page-'+str(pageindex)
    print(url)
    browser.get(url)
    elementdoc=browser.page_source
    parse_element(elementdoc)

def parse_element(html):
    doc=pq(html)
    uls = doc('.commentlist')
    divrow=uls.find('.row').items()
    for item in divrow:
        # print(item)
        strUrl=item.find('.text .view_img_link').attr('href')
        itemId=item.find('.text .righttext').text()
        if strUrl!=None:
            print(itemId)
            newurl='http:'+strUrl
            print(newurl)
            download_image(itemId,newurl)
        # newitem={
        #     'author':item.find('.author').text(),
        #     'itemid':item.find('.text .righttext').text(),
        #     'image':item.find('.text .view_img_link').attr('href')
        # }
        # print(newitem)

def download_image(id,url):
    print('Downloading', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            save_image(id,response.content)
        return None
    except ConnectionError:
        return None

def save_image(itemid,content):
    file_path = '/Users/commai/Documents/spider_pic/'+itemid+'jpg'
    print(file_path)
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


if __name__ == '__main__':

    openJiandan(49)
