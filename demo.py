#coding=utf-8

from urllib.request import urlopen
from urllib.parse import quote 
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import hashlib
import sys
import string
import time
import random
import re
import urllib

from user_agents import user_agents
from db import CrawlerDB

def extractMediaExpireDate(raw):
	now = datetime.today()
	
	mediaInfo = raw.split("-")[0].strip() 
	rawTimeInfo = raw.split("-")[1].strip()
	timeClapse = ''
	if "hour" in rawTimeInfo or "小时" in rawTimeInfo:
		timeClapse = timedelta(hours = (24 - int(rawTimeInfo.split(" ")[0])))
	elif "minute" in rawTimeInfo or "分钟" in rawTimeInfo:
		timeClapse = timedelta(minutes = (24 * 60 - int(rawTimeInfo.split(" ")[0])))
	else:
		timeClapse = timedelta(minutes = 0)
	expireDate = now + timeClapse
	
	return (mediaInfo, expireDate.isoformat())

with open('data.txt','w') as f:
	key_word = []
	crawlerDB = CrawlerDB()
	with open('key_word.txt','r') as kf:
		for line in kf:
			url = 'https://www.google.com.hk/search?q=' + line.strip() + '&source=lnms&tbm=nws&num=5'
			
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
				time.mktime(datetime.now().timetuple())) for (t1, t2) in zippedData]
			print(data)

			news_ID_list = crawlerDB.insertNewsBatch(data)

			# for item in data:
			# 	# f.writelines(''.join(item.strip().split()) + '\n')
			# 	f.writelines(''.join(item[0].strip()) + '\n')
			# 	f.writelines(''.join(item[1].strip()) + '\n')
