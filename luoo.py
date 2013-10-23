#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import sys
import xml.etree.ElementTree as ET

import common

xml_url_1 = 'http://www.luoo.net/radio/radio%d/mp3.xml'
xml_url_2 = 'http://www.luoo.net/radio/radio%d/mp3player.xml'

referer = 'http://www.luoo.net/radio/radio%d/mp3player.html'

TARGET = '/home/spyth/Music/luoo/%d'
if common.os.sys.platform.find('win') != -1:
    TARGET = 'E:\\Music\\luoo\\%d'

def extract(html):
    if not html :
        return
    root = ET.fromstring(html)
    li = []
    for song in root:
        title = song.get('title')
        location = song.get('path')
        li.append((title, location))
    return li

def download_show(li):
    for num in li:
        if num > 296: 
            url = xml_url_1%num
        else:
            url = xml_url_2%num 
        xml_data = common.open_url(url)
        if xml_data:
            songlist = extract(xml_data)
            target_dir = TARGET%num
            for title, location in songlist:
                ext = location.split('.')[-1]
                common.download(location, target_dir, title, ext, Referer=referer%num)

def main():
    if len(sys.argv) >= 2:
        try:
            li = map(int, sys.argv[1:])
        except:
            print 'Input Error!'
            return
        download_show(li)
    else:
        print u"输入期号下载,','分开.'q'退出"
        while 1:
            comm = raw_input('Select:')
            if comm == 'q':
                return
            try:
                li = map(int, comm.split(','))
            except:
                print 'Input Error!'
                continue
            download_show(li)    
if __name__ == '__main__':
    main()
