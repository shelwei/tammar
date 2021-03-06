#-*- coding: UTF-8 -*- 
import os
import sys
import jieba
import jieba.analyse
import re
import requests
from multiprocessing.dummy import Pool as ThreadPool 
from lxml import etree

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
	try:
		page = etree.HTML(html.lower())
		title = page.xpath(u'/html/head/title')[0].text
		keyword = page.xpath('/html/head/meta[@name="keywords"]/@content')[0]
		description = page.xpath('/html/head/meta[@name="description"]/@content')[0]
		
		return title, keyword, description

	except UnicodeEncodeError:
		print 'Unicode Encode Error'
	except:
		print response.headers.get('content-type')

def extract_tags(content):
	return jieba.analyse.extract_tags(content, 5)

def multi_process(urls):
	pool = ThreadPool(4)
	results = pool.map(fetch_url, urls)
	for result in results:
		content = ";".join(result)
		tags = extract_tags(content)
		print ",".join(tags)

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
	multi_process(urls)