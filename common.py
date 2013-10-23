#!/usr/bin/env python
#-*- encoding:utf8 -*-
import urllib2
import sys
import os
#import socket

#socket.setdefaulttimeout(10.0)
_myUA = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.66 Safari/537.36'

def url_request(url, UA, Referer, timeout=10):
    req = urllib2.Request(url)
    if UA:
        req.add_header('User-agent', UA)
    if Referer:
        req.add_header('Referer', Referer)
    try:
        resp = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        print '##Oops.Error:', e.code
        return
    except urllib2.URLError, e:
        print '##Oops.Error:', e.reason
        return
    except ValueError:
        print '##Oops.Url:',url
        return
    except:
        print '##Oops.Error'
        return
    return resp

def check_filepath(path, filename, ext, size):
    if not os.path.exists(path):
        os.makedirs(path)
    # replace illegal characters
    filename = filter(lambda x: x not in '\\/:*?"<>|', filename)
    is_exists = False
    if os.path.exists(os.path.join(path, '%s.%s'%(filename, ext))):
        if os.path.getsize(os.path.join(path, '%s.%s'%(filename, ext))) != size:
            i = 1
            while os.path.exists(os.path.join(path, '%s(%d).%s'%(filename, i, ext))):
                i += 1
            filename = '%s(%d)'%(filename, i)
        else:
            is_exists = True
    file_path = os.path.join(path, '%s.%s'%(filename, ext))
    return (is_exists, filename, file_path)


def open_url(url, UA=_myUA, Referer=None):
    resp = url_request(url, UA, Referer)
    if not resp:
        return
    buf = resp.read()
    return buf

def download(url, path, filename, ext, UA=_myUA, Referer=None):
    resp = url_request(url, UA, Referer)
    if not resp:
        return
    size = int(resp.headers['content-length']) 
    is_exists, filename, file_path = check_filepath(path, filename, ext, size)
    if is_exists:
        print '##File Already Exists'
        return
    bar = ProcessBar(size)
    #print filename may get encode error
    print 'Downloading [%s.%s] %.2fMB'%(filename, ext, size/1024*1.0/1024)
    with open(file_path, 'wb') as fd:
        while True:
            try:
                # control c
                # FIXME: timeout
                buf = resp.read(256)
            except:
                break
            if not buf:
                bar.done()
                return
            fd.write(buf)
            bar.update(len(buf))
    cmd = raw_input('\nRetry?(Y/n)').lower()
    if cmd == 'y':
        os.remove(file_path)
        download(url, path, filename, ext)

class ProcessBar(object):
    def __init__(self, total_size):
        self.total_size = total_size
        self.received_size = 0
    def update(self, received):
        self.received_size += received
        percent = self.received_size*1.0/self.total_size
        tmp = int(percent * 100)
        dots = '='*(tmp//2) + '-'*(tmp%2)
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
