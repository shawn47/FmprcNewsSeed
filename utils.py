#coding=utf-8

from datetime import datetime
from datetime import timedelta
import string
import time

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
