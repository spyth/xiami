#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import math
import urllib
import xml.etree.ElementTree as etree
import sys

import common

_trackUrl = 'http://www.xiami.com/song/playlist/id/%s'
_albumUrl = 'http://www.xiami.com/song/playlist/id/%s/type/1'
_collectUrl = 'http://www.xiami.com/song/playlist/id/%s/type/3'

TARGET = common.os.path.join(os.path.expanduser('~'), 'Music','xiami')
if common.os.sys.platform.find('win') != -1:
    TARGET = 'E:\\Music\\xiami'

def parse_url(loc):
    '''Parse the uri of the mp3'''
    line = int(loc[0])
    length = len(loc) - 1
    numz = int(math.ceil(length*1.0/line))
    numd = int(math.floor(length*1.0/line))
    mod = length%line
    npl = [0] + [numz]*mod + [numd]*(line-mod-1)
    uri = ""
    for i in range(1,numz+1):
        cnt = i
        if i != numz:
            for n in npl:
                cnt += n
                uri += loc[cnt]
        else:
            if mod == 0: mod=line
            for j in range(0,mod):
                cnt += npl[j]
                uri += loc[cnt]
    uri = urllib.unquote(uri).replace('^','0')
    return uri

def extract(html):
    ''' extract the xml'''
    if not html:
        return ''
    xns = '{http://xspf.org/ns/0/}%s'
    playlist = etree.fromstring(html)
    tracklist = playlist.find(xns % 'trackList')
    res = []
    for track in tracklist:
        title = track.find(xns % 'title')
        if title is None:
            break
        title = title.text.strip()
        uri = parse_url(track.find(xns % 'location').text.strip())
        lrc = track.find(xns % 'lyric').text.strip()
        if not lrc.endswith('lrc'):
            lrc = ''
        res.append((title,uri,lrc))
    return res


def main():
    if len(sys.argv) < 3 or (sys.argv[1] != '-t' and len(sys.argv) > 3):
        help_info()
        return
    if sys.argv[1] == '-a':
        url = _albumUrl % sys.argv[2]
    elif sys.argv[1] == '-c':
        url = _collectUrl % sys.argv[2]
    elif sys.argv[1] == '-t':
        url = _trackUrl % ','.join(sys.argv[2:])
    else :
        help_info()
        return
    content = common.open_url(url)
    if not content:
        return
    res = extract(content)
    for title,uri,lrc in res:
        common.download(uri,TARGET,title,'mp3')
        if lrc:
            #download the lyric

def help_info():
    print '.................USAGE....................'
    print '>xiami -a album_id'
    print '>xiami -c collection_id'
    print '>xiami -t track_id1 track_id2 track_id3...'
    print '>xiami -h'
    print '..........................................'

if __name__ == '__main__':
    main()
