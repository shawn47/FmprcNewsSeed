#coding=utf-8
from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import string
import random
import re
import urllib
import hashlib
import time

from user_agents import user_agents
from utils import extractMediaExpireDate
from db import CrawlerDB

def extractNewsByCountry(keyWord):
	keyWordArr = keyWord.split(" ")
	searchWord = keyWordArr[0]
	countryA = None if len(keyWordArr) < 2 else keyWordArr[1]
	countryB = None if len(keyWordArr) < 3 else keyWordArr[2]

	url = 'https://www.google.com.hk/search?q=' + searchWord.strip() + '&source=lnms&tbm=nws&num=20&as_qdr=n10'
	request = quote(url, safe = string.printable)
	print(request)

	index = random.randint(0, 9)
	user_agent = user_agents[index]

	headers = {'User-Agent': user_agent}
	req = urllib.request.Request(url = request, headers = headers)
	response = urllib.request.urlopen(req)

	soup = BeautifulSoup(response.read())

	titleAndUrl = [(re.sub(u'<[\d\D]*?>', ' ', str(item)), item['href']) for item in soup.select('div#ires div.g h3 > a')]

	rawSourceAndTime = [re.sub(u'<[\d\D]*?>', ' ', str(item)) for item in soup.select('div#ires div.g div.slp')]
	sourceAndTime = [extractMediaExpireDate(item) for item in rawSourceAndTime]

	zippedData = list(zip(titleAndUrl, sourceAndTime))
	data = [ ((str(t1[0]).strip(),) + 
		(hashlib.md5(str(t1[0]).strip().encode(encoding='utf-8')).hexdigest(),) + 
		(t1[1],) + t2 + 
		# (time.mktime(datetime.now().timetuple()),)) for (t1, t2) in zippedData]
		# (datetime.now().timestamp(),)) for (t1, t2) in zippedData]
		(datetime.now(),) + (countryA, ) + (countryB, )) for (t1, t2) in zippedData]
	# print(data)
	crawlerDB = CrawlerDB()
	news_ID_list = crawlerDB.insertNewsBatch(data)
	print(news_ID_list)
	print("=========")
