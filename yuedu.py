#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import json

import common

_listUrl = 'http://yuedu.fm/?data=playlist'

_itemUrl = 'http://yuedu.fm/?data=item&item_id=%d'

_TARGET = './yuedu'

def main():
    print '正在努力请求节目单...'
    data = common.open_url(_listUrl)
    if not data:
        return
    menu_list = json.loads(data)['list']

    list_format = u'[{title}] by {author}  |  {player} {min:02}:{sec:02}'

    print '{0:*^80}'.format('悦读FM.倾听文字的声音')
    print '%d 期.最新10期:'%len(menu_list)
    
    for i in range(0,10):
        print i,list_format.format(**menu_list[i])
    print "\n输入序号下载，以','分开.'q'退出"

    while True:
        usr_input = raw_input('Select(0-%d):' % (len(menu_list)-1))
        if usr_input == 'q':
            print 'bye!'
            break
        try:
            li = map(int, usr_input.split(','))
        except:
            print 'Error!\nbye!'
        for i in li:
            if i >= 0 and i < len(menu_list):
                common.download(menu_list[i]['mp3'], _TARGET, menu_list[i]['title'], 'mp3')

if __name__ == '__main__':
    main()
