# coding = utf-8

from dxspider import bdimage

if __name__ == '__main__':
    img_spider = bdimage.BDImage()
    img_spider.get_first_levels()
    img_spider.print_first_levels()
