#!/usr/bin/env python
#-*- encoding:utf-8 -*-

import sys
import xml.etree.ElementTree as ET

import common

xmlUrl_1 = 'http://www.luoo.net/radio/radio%d/mp3.xml'
xmlUrl_2 = 'http://www.luoo.net/radio/radio%d/mp3player.xml'

referer = 'http://www.luoo.net/radio/radio%d/mp3player.html'

TARGET = './luoo'

def extract(html):
    if not html :
        return
    root = ET.fromstring(html)
    li = []
    for song in root:
        title = song.get('title')
        location = song.get('path')
        li.append((title,location))
    return li

def download_show(li):
    for num in li:
        if num > 296: 
            url = xmlUrl_1 % num
        else:
            url = xmlUrl_2 % num 
        xml_data = common.open_url(url)
        if xml_data:
            songlist = extract(xml_data)
            for title, location in songlist:
                ext = location.split('.')[-1]
                common.download(location, TARGET, title, ext, Referer = referer % num)

def main():
    if len(sys.argv) >= 2:
        try:
            li = map(int, sys.argv[1:])
        except:
            print 'Inout Error!'
            return
        download_show(li)
    else:
        print "输入期号下载,','分开.'q'退出"
        while True:
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
