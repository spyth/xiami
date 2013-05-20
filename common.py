#!/usr/bin/env python
#-*- encoding:utf8 -*-
import urllib2
import sys
import os

_myUA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31'

def open_url(url, UA=_myUA, Referer=None):
    req = urllib2.Request(url)
    if UA:
        req.add_header('User-agent', UA)
    if Referer:
        req.add_header('Referer', Referer)
    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'Oops.Error:', e.code
        return
    except urllib2.URLError, e:
        print 'Oops.Error:', e.reason
        return
    buf = resp.read()
    return buf


def download(url, path, filename, ext, UA=_myUA, Referer=None):
    req = urllib2.Request(url)
    if UA:
        req.add_header('User-agent', UA)
    if Referer:
        req.add_header('Referer', Referer)
    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print 'oOps.Error:', e.code
        return
    except urllib2.URLError, e:
        print 'oOps.Error:', e.reason
        return

    if not os.path.exists(path):
        os.mkdir(path)
    if os.path.exists('%s/%s.%s' % (path, filename, ext)):
        print '%s.%s Already Exist.' % (filename, ext)
        return

    size = int(resp.headers['content-length']) 

    bar = ProcessBar(size)
    print 'Downloading [%s.%s] %.2fMB ' % (filename, ext, size/1024*1.0/1024)
    with open('%s/%s.%s' % (path, filename, ext),'wb') as fd:
        while True:
            buf = resp.read(1024)
            if not buf:
                break
            fd.write(buf)
            bar.update(len(buf))
    bar.done()


class ProcessBar():
    def __init__(self, total_size):
        self.total_size = total_size
        self.received_size = 0
    def update(self, received):
        self.received_size += received
        percent = self.received_size * 1.0 / self.total_size
        tmp = int(percent * 100)
        dots = '=' * (tmp//2) + '-' * (tmp%2)

        bar = '{0:>6.1%}[{1:<50}]'.format(percent, dots)
        sys.stdout.write('\r'+bar)
        sys.stdout.flush()
    def done(self):
        print '\nDone!'

if __name__ == '__main__':
    #url = 'http://whatsmyuseragent.com/'
    #print open_url(url)
    url = 'http://cdimage.debian.org/debian-cd/7.0.0-live/i386/webboot/debian-live-7.0.0-i386-rescue.initrd1.img'
    download(url,'./','debian','img')
