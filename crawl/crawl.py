# -*- coding:utf-8 -*-
import urllib2
import urlparse
import re
import os
import threading
import time
import sys
try:
    from BeautifulSoup import BeautifulSoup as bsoup
except:
    from bs4 import BeautifulSoup as bsoup
reload(sys)
sys.setdefaultencoding('utf8')


def simplify(s):
    s = s.split(u'logo')[0]
    s = s.split(u'LOGO')[0]
    s = s.split(u'Logo')[0]
    s = s.split(u'标识')[0]
    s = s.split(u'新标识')[0]
    s = s.split(u'标志')[0]
    s = s.split(u'新标志')[0]
    s = s.split(u'矢量')[0]
    s = s.split(u'设计欣赏')[0]
    s = s.split(u'新商标')[0]
    s = s.split(u'字体设计')[0]
    s = s.split(u'商标')[0]
    s = s.split(u'设计含义')[0]
    s = s.split(u'图片')[0]
    return s


def get_page(page):
    content = ''
    imgurl = ''
    title = ''
    img_binary = ''
    tags = []
    explain = ''
    try:
        content = urllib2.urlopen(page, timeout=2).read()
        try:
            soup = bsoup(content, 'lxml')
        except:
            soup = bsoup(content, 'html.parser')
        tmp1 = soup.findAll('div', {'class': 'detail_image'})[0]
        tmp2 = soup.find('div', {'id': 'miaoshu'})
        tmp3 = soup.find(
            'div', {'id': 'detail_additional'}).contents[-2]

        tags = re.findall("<a href=.*?>([^<]*)?</a>", unicode(tmp3))
        imgurl = tmp1.img.get('src', '')
        title = tmp1.img.get('title', '')
        explain = tmp2.p.text
        if explain == '' or explain == None:
            explain = title
        title = simplify(title)
        req = urllib2.Request(url=imgurl, headers={"Referer": page})
        img_binary = urllib2.urlopen(req).read()
    except Exception, e:
        print e
        return False, '', '', '', '', ''
    if title == '' or img_binary == '' or img_binary == None or explain == '' or tags == []:
        return False, '', '', '', '', ''
    return True, title, tags, explain, img_binary, imgurl


def add_page_to_folder(picNum, img_binary, title, tags, explain, imgurl, page):
    index_filename = os.path.join(BASE_PATH, 'PICTURES.txt')
    title_filename = os.path.join(BASE_PATH, "TITLES.txt")
    global folder
    filename = str(picNum).zfill(5) + '.' + imgurl.split('.')[-1]
    if not os.path.exists(folder):
        os.mkdir(folder)
    pathtmp = os.path.join(folder, filename)
    img = open(pathtmp, 'wb')
    img.write(img_binary)
    img.close()

    varLock.acquire()
    index = open(index_filename, 'a')
    index.write(u'\t'.join([unicode(picNum), title, explain, '%'.join(tags), imgurl, filename, page]))
    index.write(u'\n')
    index.close()
    titlelist = open(title_filename, 'a')
    titlelist.write(title + u'\n')
    titlelist.close()
    varLock.release()


def crawl():
    global crawlCount, maxPage, saveCount
    while True:
        varLock.acquire()
        page = prefix + str(crawlCount).zfill(5) + '.html'
        crawlCount += 1
        # if crawled.find(page):
        #    varLock.release()
        #    continue
        # crawled.add(page)
        # varLock.release()
        # varLock.acquire()
        if saveCount < maxPage:
            varLock.release()
            success, title, tags, explain, img_binary, imgurl = get_page(
                page)
            if success:
                varLock.acquire()
                if saveCount > maxPage:
                    varLock.release()
                    return
                picNum = saveCount
                print saveCount, '##', page
                saveCount += 1
                varLock.release()
                add_page_to_folder(
                    picNum, img_binary, title, tags, explain, imgurl, page)
        else:
            varLock.release()
            return


def main(threadNum, maxPageNum):
    starttime = time.time()
    startclock = time.clock()

    # 重置全局变量
    global crawlCount, fileEnding,  maxPage, crawled, saveCount
    crawlCount = 2
    saveCount = 1
    fileEnding = 0
    #crawled = Bloom.Bloom(maxPageNum)
    maxPage = maxPageNum

    # 设置并行
    threads = []
    for i in range(threadNum):
        t = threading.Thread(target=crawl)
        t.setDaemon(True)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    if saveCount < maxPageNum:
        print 'Crawled pages may be fewer than', maxPageNum

    endtime = time.time()
    endclock = time.clock()
    duration = max(endtime - starttime, endclock - startclock)
    print '=' * 10, '\nTHREAD: %d\tPages: %d\tTIME: %.9fs'\
        % (threadNum, crawlCount, duration)


varLock = threading.Lock()
prefix = 'http://logonc.com/'
BASE_PATH = os.path.dirname(__file__)
#'thread数量、爬取图片数、文件夹存放图片
thread_num = 10
max_pics = 20000
folder = os.path.join(BASE_PATH, 'pic')


main(thread_num, max_pics)
a = raw_input()
