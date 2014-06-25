#-*- coding: UTF-8 -*- 
import os
import sys
import jieba
import jieba.analyse
import re
import urllib2
import chardet
from multiprocessing.dummy import Pool as ThreadPool 
from lxml import etree
import timeit

reload(sys)    
sys.setdefaultencoding('utf-8')

def extract_url(bookmark_filepath):
	f = open(bookmark_filepath, 'rb')
	html = f.read()
	regx = '((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*))'

	rg = re.compile(regx,re.IGNORECASE|re.DOTALL)
	return rg.findall(html)

def fetch_url(url):
	response = urllib2.urlopen(url)
	html = response.read()
	content_type = response.headers.get('content-type')
	#print content_type
	if(html):
		encode = chardet.detect(html)['encoding']
		if encode == 'GB2312':
			encode = 'gbk'
		if not encode:
			encode = 'utf-8'
		'''	
		page = etree.HTML(html.lower().decode(encode))
		title = page.xpath(u'/html/head/title')
		keyword = page.xpath('/html/head/meta[@name="keywords"]/@content')
		description = page.xpath('/html/head/meta[@name="description"]/@content')
		print title[0].text
		print keyword[0]
		print description[0]
		'''
		#print encode

def multi_process(urls):
	pool = ThreadPool(4)
	results = pool.map(fetch_url, urls)
	pool.close()
	pool.join

def single_process(urls):
	for url in urls:
		fetch_url(url)

if __name__ == '__main__':
	#urls = extract_url('./bookmarks_14-6-24.html');
	urls = [
		'http://www.sohu.com',
		'http://www.sina.com.cn',
		'http://www.qq.com'
	]
	t1 = timeit.Timer("multi_process(urls)", "from __main__ import multi_process, urls")
	t2 = timeit.Timer("single_process(urls)", "from __main__ import single_process, urls")
	print 'multi_process',t1.timeit(1)
	print 'single_process',t2.timeit(1)