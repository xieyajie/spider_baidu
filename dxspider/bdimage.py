# coding = utf-8

'''
使用正则表达式查找

提供以下功能:
1. 获取百度图库一级分类
2. 获取百度图库 "壁纸"分类
3. 获取"壁纸"分类下的图片原始链接
'''

from urllib import parse
from urllib import request
# from bs4 import BeautifulSoup
import re
import os
import socket
import datetime
# import threading

IMAGE_BASE_URL = "http://image.baidu.com/"

headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
    # 'Cookie': 'HMACCOUNT=3F8A217F8782851F; BDUSS=VhalA1QVZBbDJKaFlsc3hyYXl3ZUM1OEpIVkdZS0FtaUVMNUZhblo5OFUxeTFYQVFBQUFBJCQAAAAAAAAAAAEAAACEaL0geHlqeHlmMTIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABRKBlcUSgZXaU; BAIDUID=ED38E8994B2AB55469EB685F4A982CD3:FG=1; PSTM=1461059981; BIDUPSID=E1CC56ACEEB7A85025A35FD731910788; MCITY=-131%3A; BDSFRCVID=j_-sJeCCxG3xlL3Ryw9QaM0wkAgKzEfwrxqH3J; H_BDCLCKID_SF=JRAjoK-XJDv8fJ6xq4vhh4oHjHAX5-RLfK_DKtOF5lOTJh0R2-RWKlD-eJjJW5vnJJTiLb5aQb3dbqQRK5bke6oWeHKtJ6LsKDLX3Rr_bRvqKROvhjR8BIuyyxom3bvxt5bQ2IO4M40BVJjEDbJOLt-U24oh-bjO-m-eaDcJ-J8XhD-GjjrP; H_PS_PSSID=17944; HMVT=737dbb498415dd39d8abf5bc2404b290|1461386196|; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm'
    }

class BDImage(object):

    def __init__(self):
        self.tasks = []
        self.first_levels = {}
        self.wallpaper_url = None
        self.wallpaper_levels = {}

    '''
    统一的request接口
    '''
    def request_url(self, url, headers={}, data=None, method=None):
        if url is None:
            return None

        socket.setdefaulttimeout(10)
        req = request.Request(url, headers=headers, data=data, method=method)

        respon_data = None
        try:
            respon = request.urlopen(req)
            respon_data = respon.read()
        except:
            print("error")

        respon = None
        if respon_data is not None:
            try:
                respon = respon_data.decode('utf-8', errors="ignore")
            except:
                try:
                    respon = respon_data.decode('gb2312', errors="ignore")
                except:
                    respon = respon_data

        return respon

    '''
    打印百度图库一级分类
    '''
    def print_first_levels(self):
        print('First Levels:\n')
        if len(self.first_levels) > 0:
            print(''.join('{level}\n'.format(level = level) for level in self.first_levels))

    '''
    获取百度图库一级分类
    '''
    def get_first_levels(self):
        respon_data = self.request_url(IMAGE_BASE_URL, headers=headers, method='GET')
        if respon_data is None:
            return None

        self.first_levels = {}
        pattern = re.compile('<a class=\"img_link_layer\" href=[\w\s\d\-\.\"=&:;%\?\/\#\$\“\”\!\@\^\*]*>\s*<div class=\"img_instr_layer\">\S*</div>')
        all_values = pattern.findall(respon_data)

        for value in all_values:
            href_pattern = re.compile('href=\"\S*\"')
            href = href_pattern.findall(value)[0]
            href = href.replace('href=\"', '')
            href = href[:len(href) - 1]
            href = href.replace('&amp;', '&')

            tag_pattern = re.compile('<div class=\"img_instr_layer\">\S*</div>')
            classify = tag_pattern.findall(value)[0]
            classify = classify.replace('<div class=\"img_instr_layer\">', '')
            classify = classify.replace('</div>', '')

            self.first_levels[classify] = href

        return self.first_levels

    '''
    打印百度图库 "壁纸"分类
    '''
    def print_wallpaper_levels(self):
        print('Wallpaper Levels:\n')
        if len(self.wallpaper_levels) > 0:
            for level2 in self.wallpaper_levels:
                print(level2 + ':\n')
                print(''.join('\t{level3}\n'.format(level3 = level3) for level3 in self.wallpaper_levels[level2]))

    '''
    获取百度图库 "壁纸"分类
    '''
    def get_wallpaper_levels(self):
        if self.wallpaper_url is None:
            if self.first_levels is None or len(self.first_levels) == 0:
                self.get_first_levels()
            if self.first_levels is not None:
                self.wallpaper_url = self.first_levels['壁纸']

        respon_data = self.request_url(self.wallpaper_url, headers=headers, method='GET')
        if respon_data is None:
            return None

        self.wallpaper_levels = {}
        level2_pattern = re.compile(u'name:\"\s*\w+\s+\w+\"')
        level2_list = level2_pattern.findall(respon_data)
        for level2 in level2_list:
            item = level2.replace('name:', '')
            item = item.replace('\"', '')
            if item not in self.wallpaper_levels:
                self.wallpaper_levels[item] = []

        level3_pattern = re.compile(u'name:\"\s*\w+\s+\w+\s+\w+\"')
        level3_list = level3_pattern.findall(respon_data)
        for level3 in level3_list:
            item = level3.replace('name:', '')
            item = item.replace('\"', '')
            for level2 in self.wallpaper_levels:
                if item.find(level2) != -1:
                    self.wallpaper_levels[level2].append(item)

        return self.wallpaper_levels

    '''
    获取"壁纸"分类下的图片原始链接
    '''
    def get_wallpaper_urls(self, word=None, width=1440, height=900, curser=0, page_num=60):
        if word is None:
            word = ""
        if width is None or height is None:
            width = ""
            height = ""

        word_str = parse.urlencode({'word': word})
        url = "http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&" \
              + word_str + "&cg=wallpaper&pn=" + str(curser) + "&rn=" + str(page_num) \
              + "&itg=1&z=0&fr=&width=" + str(width) + "&height=" + str(height) \
              + "&lm=-1&ic=&s=0&st=-1&gsm=78"
        resp_data = self.request_url(url, headers, method='GET')

        name_pattern = re.compile(u'\"nam e\":\"\w+\s+\w+\s+\w+\"')
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

    '''
    下载图片
    '''
    def download_images(self, urls, save_dir):
        index = 0
        for url in urls:
            end = os.path.splitext(url)[1]
            if len(end) == 0:
                    end = ".jpg"
            img_path = save_dir + str(datetime.datetime.now().microsecond) + '_%i%s' % (index, end)
            try:
                image = request.urlretrieve(url, img_path)
                index += 1
            except Exception as e:
                print(e)
                pass
