#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import json
import sys
import codecs

import common

list_url = 'http://yuedu.fm/?data=playlist'
item_url = 'http://yuedu.fm/?data=item&item_id=%d'

_TARGET = common.os.path.join(os.path.expanduser('~'), 'Music','yuedu')
if common.os.sys.platform.find('win') != -1:
    _TARGET = 'E:\\Music\\yuedu'


def main():
    sys.stdout.write(u'正在努力请求节目单...')
    sys.stdout.flush()
    data = common.open_url(list_url)
    if not data:
        return
    menu_list = json.loads(data)['list']
    sys.stdout.write('\r')

    list_format = u'[{title}] by {author}  |  {player} {min:02}:{sec:02}'
    print u'{0:*^60}'.format(u'悦读FM.倾听文字的声音')
    print u'总共%d期.最新10期:'%len(menu_list)

    for i in range(0,10):
        print i,list_format.format(**menu_list[i])
    print u"\n输入序号下载，以','分开.'q'退出"

    while 1:
        usr_input = raw_input('Select(0-%d):'%(len(menu_list)-1))
        if usr_input == 'q':
            print 'bye!'
            break
        try:
            li = map(int, usr_input.split(','))
        except:
            print 'Input Error!'
        for i in li:
            if 0 <= i < len(menu_list):
                common.download(menu_list[i]['mp3'], _TARGET,\
                    menu_list[i]['title'], 'mp3', Referer='http://yuedu.fm/')
                article2Html(i, menu_list[i]['title'])

def article2Html(num, filename):
    data = common.open_url(item_url%num) 
    item = json.loads(data)['item'][0]
    #common.download(item['bg'], _TARGET, filename, 'jpg') 
    with codecs.open('%s/%s.html'%(_TARGET, filename), 'w', 'utf-8') as fd:
        fd.write('<!DOCTYPE html><html><head><meta charset="utf-8"/></head><body>')
        fd.write(item['text'])
        fd.write('</body></html>')

if __name__ == '__main__':
    main()
