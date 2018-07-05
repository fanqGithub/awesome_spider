import requests
from bs4 import BeautifulSoup

index = 0
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}

def qiushibaike():
    content = requests.get('http://www.qiushibaike.com').content
    soup = BeautifulSoup(content, 'html.parser')

    for div in soup.find_all('div', {'class' : 'content'}):
        print (div.text.strip())

def ustcjob():
    headers = {'User-Agent':'Mozilla / 5.0(X11;Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 50.0.2661.102 Safari / 537.36'}
    content = requests.get('http://job.ustc.edu.cn/list.php?MenuID=002', headers = headers).content
    soup = BeautifulSoup(content, 'html.parser')

    for Jop in soup.find_all('div', {'class' : 'Joplistone'}):
        for item in Jop.find_all('li'):
            print ("%-30s%-20s%-40s" % (item.a.text.strip() , item.span.text.strip() , item.span.next_sibling.text.strip()))



def save_jpg(res_url):
    img_id=0
    resp=requests.get(res_url)
    soup = BeautifulSoup(resp.content,"lxml")
    # tag=soup.find('a', {'class': 'view_img_link'})
    for i in soup.select('.text'):
        print(i)
        img_url=i.find('a')['href']
        print(img_url)
        with open('./pic_' + str(img_id) + '.jpg', 'wb') as pic_file:
            pic_file.write(requests.get(img_url).content)
        img_id+=1

    # html = BeautifulSoup(requests.get(res_url, headers=headers),"html.parser")
    # for link in html.find_all('a', {'class': 'view_img_link'}):
    #     with open('{}.{}'.format(index, link.get('href')[len(link.get('href'))-3: len(link.get('href'))]), 'wb') as jpg:
    #         jpg.write(requests.get("http:" + link.get('href')).content)
    #     print("正在抓取第%s条数据" % index)
    #     index += 1


def testPic():
    pic_id = 0  # 图片编号
    url = 'http://www.ivsky.com/bizhi/stand_by_me_doraemon_v45983/'
    bs = BeautifulSoup(requests.get(url).content, "lxml")
    for i in bs.select('.il_img'):
        pic_url = i.find('img')['src']
        pic_file = open('./pic_' + str(pic_id) + '.jpg', 'wb')  # 二进制创建并写入文件
        pic_file.write(requests.get(pic_url).content)  # 写出请求得到的img资源
        pic_id += 1


if __name__ == '__main__':
    url = 'http://jandan.net/ooxx'

    # qiushibaike()

    save_jpg(url)
    #
    # testPic()

