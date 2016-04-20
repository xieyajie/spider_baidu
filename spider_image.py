# coding = utf-8

from urllib import request
from bs4 import BeautifulSoup
import re


def convert_url(tmp_url):
    if tmp_url is None or len(tmp_url) == 0:
        return None

def open_url(url, save_dir):
    if url is None or len(url) == 0:
        return None, None

    headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }


    req = request.Request(url=url, headers=headers, method='GET')
    resp = request.urlopen(req)
    resp_data = resp.read().decode('utf-8')

    name_pattern = re.compile(u'\"name\":\"\w+\s+\w+\s+\w+\"')
    all_names = name_pattern.findall(resp_data)
    ret_names = []
    for item in all_names:
        item = item.replace('\"name\":\"', '')
        item = item.replace('\"', '')
        ret_names.append(item)

    url_pattern = re.compile(r'\"objURL\":\"http://\w+[\.]\w+[\.]\w+[/\w*]*/\w*/[\w*\s*\-]+[\.]{1}\w+\"')
    all_urls = url_pattern.findall(resp_data)
    ret_urls = []
    for item in all_urls:
        item = item.replace('\"objURL\":\"', '')
        item = item.replace('\"', '')
        ret_urls.append(item)

    return ret_names, ret_urls


if __name__ == '__main__':
    # url = "http://image.baidu.com/search/index?\
    # ct=201326592&cl=2&st=-1&lm=-1&nc=1&ie=utf-8&tn=baiduimage&ipn=r&rps=1&pv=&fm=rs5&\
    # word=%E5%A3%81%E7%BA%B8&oriquery=%E5%9B%BE%E7%89%87&ofr=%E5%9B%BE%E7%89%87#z=0&\
    # pn=&ic=&st=-1&face=0&s=0&lm=-1&width=&height="

    url = "http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=%E5%A3%81%E7%BA%B8%20%E5%8D%A1%E9%80%9A%E5%8A%A8%E6%BC%AB%20%E6%B5%B7%E8%B4%BC%E7%8E%8B&cg=wallpaper&pn=0&rn=60&itg=1&z=0&fr=&width=1440&height=900&lm=-1&ic=&s=0&st=-1&gsm=78"
    save_dir = "./baidu"
    names, urls = open_url(url, save_dir)

    if urls is not None:
        print(''.join('{url}\n'.format(url = url) for url in urls))
