import json
import re
from multiprocessing import Pool

import requests
from requests.exceptions import RequestException

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

def get_one_page(url):
    try:
        response=requests.get(url,headers=headers)
        if(response.status_code==200):
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    # 后面加的re.S表示匹配任意的字符，要不然像这里面的格式，会有一些换行等字符
    pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items=re.findall(pattern,html)
    for i in items:
        yield {
            'index':i[0],
            'image':i[1],
            'title':i[2],
            'actor':i[3].strip()[3:],
            'time':i[4].strip()[5:],
            'score':i[5]+i[6]
        }
        # print(i)

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()


def start(offset):
    url='https://maoyan.com/board/4?offset='+str(offset)
    html=get_one_page(url)
    items=parse_one_page(html)
    for it in items:
        write_to_file(it)


if __name__ == '__main__':
    # 普通的使用
    # for i in range(10):
    #     start(i*10)

    #多进程的使用方式：
    pool = Pool()
    pool.map(start,[i*10 for i in range(10)])