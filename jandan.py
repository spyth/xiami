#-*- encoding:utf8 -*-
import os
import re

import common

meizi_page = 'http://jandan.net/ooxx/page-%d#comments'
meizi_default = 'http://jandan.net/ooxx'
wuliao_page = 'http://jandan.net/pic/page-%d#comments'
wuliao_default = 'http://jandan.net/pic'

TARGET = os.path.join(os.path.expanduser('~'), 'Pictures')
if os.sys.platform.find('win') != -1:
    TARGET = 'E:\\Pic'

def download_pic(url):
    print url
    html = common.open_url(url)
    find_re = re.compile(r'<li id.+?<img src="(.+?)"', re.DOTALL)
    img_url = find_re.findall(html)
    print 'Start download %d pics'%len(img_url) 
    for url in img_url:
        if url:
            filename,ext = os.path.splitext(os.path.split(url)[-1])
            if not ext:
                ext = '.jpg'
            common.download(url, TARGET, filename, ext[1:], Referer=url)

def main():
    print u'无聊图请按1，妹纸图请按2, 其它自动挂机。'
    choice = raw_input('>')
    global TARGET
    if choice == '1':
        url_default = wuliao_default
        url_page = wuliao_page
        TARGET = os.path.join(TARGET, 'jandan-pic')
    elif choice == '2':
        url_default = meizi_default
        url_page = meizi_page
        TARGET = os.path.join(TARGET, 'jandan-ooxx')
    else:
        print 'bye!'
        return
    html = common.open_url(url_default)
    find_RE = re.compile(r'>\[(.+?)\]')
    result = find_RE.findall(html)
    cur_page = int(result[0])
    print 'Current Page Number:%d'%cur_page
    cnt = int(raw_input('How many pages do you want to download? \n>'))
    for i in range(0,cnt):
        download_pic(url_page%(cur_page-i))

if __name__ == '__main__':
    main()
