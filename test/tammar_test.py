#-*- coding: UTF-8 -*- 
import os
import sys
import jieba
import jieba.analyse
import re
import requests
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
	response = requests.get(url)
	html = response.content
	#print html
	'''	
	content_type = response.headers.get('content-type')
	#print content_type
	if(html):
		encode = chardet.detect(html)['encoding']
		if encode == 'GB2312':
			encode = 'gbk'
		if not encode:
			encode = 'utf-8'
		'''
	try:
		page = etree.HTML(html.lower())
		title = page.xpath(u'/html/head/title')
		keyword = page.xpath('/html/head/meta[@name="keywords"]/@content')
		description = page.xpath('/html/head/meta[@name="description"]/@content')
		print title[0].text
		print keyword[0]
		print description[0]
	except UnicodeEncodeError:
		print 'Unicode Encode Error'
	except:
		print response.headers.get('content-type')

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
	
	#multi_process(urls)