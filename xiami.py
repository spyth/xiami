#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import math
import urllib
import xml.etree.ElementTree as etree

import sys

import requests

_baseURL = 'http://www.xiami.com/song/playlist/id/'
_album = '/type/1'
_collect = '/type/3'
TARGET = './xiami'
UA =  'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17'

def parse_url(loc):
	'''Parse the uri of the mp3'''
	line = int(loc[0])
	length = len(loc) - 1
	numz = int(math.ceil(length*1.0/line))
	numd = int(math.floor(length*1.0/line))
	mod = length%line
	
	npl = [0] + [numz] * mod + [numd] * (line-mod-1)
	uri = ""
	for i in range(1,numz+1):
		cnt = i
		if i != numz:
			for n in npl:
				cnt += n
				uri += loc[cnt]
		else:
			if mod == 0: mod = line
			for j in range(0,mod):
				cnt += npl[j]
				uri += loc[cnt]
	uri = urllib.unquote(uri).replace('^','0')
	return uri
	
def extract(html):
	if not html:
		return ''
	playlist = etree.fromstring(html)
	tracklist = playlist.find('{http://xspf.org/ns/0/}trackList')
	res = []
	for track in tracklist:
		title = track.find('{http://xspf.org/ns/0/}title')
		if title is None:
			break
		title = title.text.strip()
		uri = parse_url(track.find('{http://xspf.org/ns/0/}location').text.strip())
		lrc = track.find('{http://xspf.org/ns/0/}lyric').text.strip()
		if not lrc.endswith('lrc'):
			lrc = ''
		res.append((title,uri,lrc))
	return res

def download(url,name,ext,mode):
	session = requests.Session()
	session.headers.update({'User-Agent':UA})
	#print 'Downloading %s.%s'%(name,ext)
	rep = session.get(url)
	if rep.status_code == 200:
		fd = open('%s/%s.%s'%(TARGET,name,ext),mode)
		fd.write(rep.content)
		fd.close()
		print 'success.'
	else :
		print 'oOps.'
	
def main():
	if len(sys.argv) < 3 or (sys.argv[1] != '-t' and len(sys.argv) > 3):
		help_info()
		return
	
	if sys.argv[1] == '-a':
		url = _baseURL + sys.argv[2] + _album
	elif sys.argv[1] == '-c':
		url = _baseURL + sys.argv[2] + _collect
	elif sys.argv[1] == '-t':
		url = _baseURL + ','.join(sys.argv[2:])
	else :
		help_info()
		return
	
	r = requests.get(url)
	if r.status_code == 200:
		res = extract(r.content)
		if not os.path.exists(TARGET):
			os.mkdir(TARGET)
		if not res:
			print 'failed...'
			return
		cnt = 1
		for title,uri,lrc in res:
			#print 'title: %s\nuri: %s\nlrc: %s'%(title, uri, lrc)
			print '#%02d.mp3 downloading...'%cnt,
			download(uri,title,'mp3','wb')
			if lrc:
				print '#%02d.lrc downloading...'%cnt,
				download(lrc,title,'lrc','w')
			cnt += 1
	else:
		print 'Oops.Request Failed...'
		print 'Check The URL: %s'%url
	
def help_info():
	print '.................USAGE....................'
	print '>xiami -a album_id'
	print '>xiami -c collection_id'
	print '>xiami -t track_id1 track_id2 track_id3...'
	print '>xiami -h'
	print '..........................................'

if __name__ == '__main__':
	main()