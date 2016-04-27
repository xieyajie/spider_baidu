# coding = utf-8

from dxspider import bdimage

if __name__ == '__main__':
    img_spider = bdimage.BDImage()
    img_spider.get_first_levels()
    img_spider.print_first_levels()

    img_spider.get_wallpaper_levels()
    img_spider.print_wallpaper_levels()

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

    names, urls = img_spider.get_wallpaper_urls(word, width, height, page_num=num)
    img_spider.download_images(urls, '../wallpaper')
