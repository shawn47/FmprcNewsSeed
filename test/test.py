#coding=utf-8

from datetime import datetime
from db import CrawlerDB

from checkExpiredNews import checkExpiredNews

def dbTest():
	crawlerDB = CrawlerDB()
	now = datetime.now()
	result = crawlerDB.findExpiredNews(now)
	for x in result:
		print(x[0])

def checkExpiredNewsTest():
	now = datetime.now()
	try:
		checkExpiredNews()
	except Exception as e:
		raise e
		print(e)

if __name__ == '__main__':
	# dbTest()
	checkExpiredNewsTest()
