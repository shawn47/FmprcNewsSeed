#coding=utf-8

from datetime import datetime

from db import CrawlerDB

def checkExpiredNews():
	crawlerDB = CrawlerDB()
	now = datetime.now()
	raw_result = crawlerDB.findExpiredNews(now)
	result = [ _[0] for _ in raw_result]

	print(result)
	crawlerDB.setNewsExpired(result)
