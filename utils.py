#coding=utf-8

from datetime import datetime
from datetime import timedelta
import string
import time
import os
import random
import sys

from config import DOMAIN, USER_AGENT, ROOT_FILE

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

def getRandomDomain():
	domain = random.choice(get_data('domains.txt', DOMAIN))
	return domain

def getRandomUserAgent():
	user_agent = random.choice(get_data('user_agents.txt', USER_AGENT))
	return user_agent

def get_data(filename, default = ''):
	domain_files = os.path.join(
	    os.path.join(ROOT_FILE, 'data'), filename)
	try:
	    with open(domain_files) as fp:
	        data = [_.strip() for _ in fp.readlines()]
	except:
	    data = [default]
	return data
