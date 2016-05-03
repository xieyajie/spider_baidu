# coding = utf-8

from dxspider import bdimage
import threading

def get_images(word=None, width=1440, height=900, curser=0, page_num=60):
    urls = img_spider.get_wallpaper_urls(word, width, height, curser=curser, page_num=num)
    img_spider.download_images(urls, '../wallpaper')


def get_input():
    word = ""
    while len(word) == 0:
        word = input("输入想爬的标签,如 壁纸 不同风格 美女:\n")

    width = 1440
    wstr = input("输入壁纸宽, 默认 1440:\n")
    if len(wstr) == 0:
        width = 1440
    else:
        width = int(wstr)

    height = 900
    hstr = input("输入壁纸宽, 默认 900:\n")
    if len(hstr) == 0:
        height = 900
    else:
        height = int(hstr)

    num = 60
    nstr = input("输入个数, 默认 60:\n")
    if len(nstr) == 0:
        num = 60
    else:
        num = int(nstr)

    return word, width, height, num


def search_levels():
    img_spider.get_first_levels()
    img_spider.print_first_levels()

    word, width, height, num = get_input()
    t = threading.Thread(target=get_images, args=(word, width, height, 0, num))
    t.start()


def search_custom():
    word, width, height, num = get_input()
    urls = img_spider.search_images(word, width, height, 0, num)
    img_spider.download_images(urls, '../wallpaper')


if __name__ == '__main__':
    print("选择搜索类型:\n\t1 分类搜索\n\t2 自定义搜索\n")
    opstr = ""
    while len(opstr) == 0:
        opstr = input("输入编号: ")

    op = int(opstr)
    img_spider = bdimage.BDImage()
    if op == 1:
        search_levels()
    elif op == 2:
        search_custom()


    # img_spider.get_wallpaper_levels()
    # img_spider.print_wallpaper_levels()
    #
    # while 1:
    #     word = ""
    #     while len(word) == 0:
    #         word = input("输入想爬的标签,如 壁纸 不同风格 美女:\n")
    #
    #     width = 2880
    #     wstr = input("输入壁纸宽, 默认 2880:\n")
    #     if len(wstr) == 0:
    #         width = 2880
    #     else:
    #         width = int(wstr)
    #
    #     height = 1800
    #     hstr = input("输入壁纸宽, 默认 1800:\n")
    #     if len(hstr) == 0:
    #         height = 1800
    #     else:
    #         height = int(hstr)
    #
    #     num = 60
    #     nstr = input("输入个数, 默认 60:\n")
    #     if len(nstr) == 0:
    #         num = 60
    #     else:
    #         num = int(nstr)
    #
    #     t = threading.Thread(target=get_images, args=(word, width, height, 0, num))
    #     t.start()
