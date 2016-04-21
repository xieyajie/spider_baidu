# coding = utf-8

'''
使用正则表达式查找

提供以下功能:
1. 获取百度图库一级分类
2. 获取百度图库二级和三级分类
3. 获取各个分类下的图片原始链接
'''

from urllib import request
from bs4 import BeautifulSoup
import re
import os

IMAGE_BASE_URL = "http://image.baidu.com/"

def request_url(url, headers={}, data=None, method=None):
    if url is None:
        return None

    req = request.Request(url, headers=headers, data=data, method=method)
    respon = request.urlopen(req)
    respon_data = respon.read().decode('utf-8')

    return respon_data


def get_first_level_classification():
    respon_data = request_url(IMAGE_BASE_URL, method='GET')
    if respon_data is None:
        return None

    ret_classifys = {}
    pattern = re.compile('<a class=\"img_link_layer\" href=[\w\s\d\-\.\"=&\:\;\%\?\/\#\$\“\”\!\@\^\*]*>\s*<div class=\"img_instr_layer\">\S*</div>')
    all_values = pattern.findall(respon_data)

    for value in all_values:
        href_pattern = re.compile('href=\"\S*\"')
        href = href_pattern.findall(value)[0]
        href = href.replace('href=\"', '')
        href = href[:len(href) - 1]

        tag_pattern = re.compile('<div class=\"img_instr_layer\">\S*</div>')
        classify = tag_pattern.findall(value)[0]
        classify = classify.replace('<div class=\"img_instr_layer\">', '')
        classify = classify.replace('</div>', '')

        ret_classifys[classify] = href

    return ret_classifys

def get_wallpaper_levels(url):
    respon_data = request_url(url, 'GET')
    if respon_data is None:
        return None

    ret_levels = {}
    pattern = re.compile('')


def convert_url(tmp_url):
    if tmp_url is None or len(tmp_url) == 0:
        return None

def open_url(url):
    if url is None or len(url) == 0:
        return None, None

    headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }

    resp_data = request_url(url, headers, method='GET')

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

def get_images(urls, save_dir):
    index = 0
    for url in urls:
        end = os.path.splitext(url)[1]
        if len(end) == 0:
                end = ".jpg"
        img_path = save_dir + '%i%s' % (index, end)
        image = request.urlretrieve(url, img_path)
        index = index + 1


if __name__ == '__main__':
    # 1. 获取百度图库一级分类
    first_levels = get_first_level_classification()
    if first_levels is not None:
        print('First Levels:\n')
        print(''.join('{level}\n'.format(level = level) for level in first_levels))

    # 2. 获取"壁纸"分类下的子分类
    wallpaper_url = first_levels['壁纸']
    if wallpaper_url is not None:
        wallpaper_levels = get_wallpaper_levels(wallpaper_url)

    # url = "http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=%E5%A3%81%E7%BA%B8%20%E5%8D%A1%E9%80%9A%E5%8A%A8%E6%BC%AB%20%E6%B5%B7%E8%B4%BC%E7%8E%8B&cg=wallpaper&pn=0&rn=60&itg=1&z=0&fr=&width=1440&height=900&lm=-1&ic=&s=0&st=-1&gsm=78"
    # names, urls = open_url(url)
    #
    # if urls is not None:
    #     print(''.join('{url}\n'.format(url = url) for url in urls))
    #
    # save_dir = "./baidu"
    # get_images(urls, save_dir)
